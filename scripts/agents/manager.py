#!/usr/bin/env python3
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, request


ROOT = Path(__file__).resolve().parents[2]
TASKS_DIR = ROOT / "tasks"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(load_text(path))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=4) + "\n", encoding="utf-8")


def list_task_dirs() -> list[Path]:
    if not TASKS_DIR.exists():
        return []
    return sorted([path for path in TASKS_DIR.iterdir() if path.is_dir()])


def pick_task(task_dirs: list[Path], prompt: str) -> Path | None:
    lowered_prompt = prompt.lower()

    for task_dir in task_dirs:
        if task_dir.name.lower() in lowered_prompt:
            return task_dir

    task_match = re.search(r"(task-\d+)", lowered_prompt)
    if task_match:
        prefix = task_match.group(1)
        for task_dir in task_dirs:
            if task_dir.name.lower().startswith(prefix):
                return task_dir

    for task_dir in task_dirs:
        journal_path = task_dir / "agents-journal.json"
        if not journal_path.exists():
            return task_dir
        journal = load_json(journal_path).get("journal", [])
        has_manager_entry = any(entry.get("agent") == "Manager" and entry.get("timestamp") for entry in journal)
        if not has_manager_entry:
            return task_dir

    return task_dirs[0] if task_dirs else None


def call_model(prompt: str, description: str, task_name: str) -> str:
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        raise RuntimeError("GITHUB_TOKEN is required")

    system_prompt = (
        "You are the Manager agent for a software repository. "
        "Review one task and decide if it is ready for implementation by the Coder. "
        "Respond in plain text with exactly three lines:\n"
        "Decision: <ready|blocked>\n"
        "Summary: <short summary>\n"
        "Next: <short next step>"
    )
    user_prompt = (
        f"Manager instruction: {prompt}\n\n"
        f"Task folder: {task_name}\n\n"
        f"Task description:\n{description}"
    )

    payload = {
        "model": "openai/gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        "https://models.github.ai/inference/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {github_token}",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub Models request failed: {exc.code} {message}") from exc

    data = json.loads(raw)
    return data["choices"][0]["message"]["content"].strip()


def append_manager_entry(journal_path: Path, task_name: str, prompt: str, response: str) -> None:
    if journal_path.exists():
        journal_data = load_json(journal_path)
    else:
        journal_data = {"journal": []}

    journal = journal_data.setdefault("journal", [])
    if len(journal) == 1 and not any(journal[0].values()):
        journal.clear()

    journal.append(
        {
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "agent": "Manager",
            "entry": f"Reviewed {task_name} and prepared it for the next workflow stage",
            "details": f"Prompt: {prompt}\n\nManager response:\n{response}",
        }
    )
    save_json(journal_path, journal_data)


def main() -> int:
    prompt = os.environ.get("MANAGER_PROMPT", "").strip()
    if not prompt:
        print("MANAGER_PROMPT is required", file=sys.stderr)
        return 1

    task_dirs = list_task_dirs()
    if not task_dirs:
        print("No task folders found in tasks/", file=sys.stderr)
        return 1

    task_dir = pick_task(task_dirs, prompt)
    if task_dir is None:
        print("No task could be selected", file=sys.stderr)
        return 1

    description_path = task_dir / "description.md"
    journal_path = task_dir / "agents-journal.json"
    if not description_path.exists():
        print(f"Task description is missing for {task_dir.name}", file=sys.stderr)
        return 1

    description = load_text(description_path)
    response = call_model(prompt, description, task_dir.name)
    append_manager_entry(journal_path, task_dir.name, prompt, response)

    print(f"Selected task: {task_dir.name}")
    print(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
