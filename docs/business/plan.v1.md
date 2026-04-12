# Business Plan v1

## Purpose

Lessons Dashboard is a web application for online teachers. The goal is to give teachers a single place to manage lesson preparation, student progress, lesson delivery, and scheduling.

This document captures the current product idea. It is intentionally versioned as `v1` because requirements may change during planning and implementation.

## Product Goals

### Primary Goal

Build a reliable web app that helps online teachers with day-to-day teaching work.

### Secondary Goal

Build the product with an AI-agent-driven delivery model, where the human user defines tasks and agents execute the implementation workflow in cloud automation.

## Core Users

### Teachers

Teachers are the main users of the platform. They need tools to plan lessons, manage students, share materials, and keep their schedule under control.

### Students

Students interact with lessons and materials that are shared by teachers. They may use the product as registered users or access specific lessons through secure teacher-generated links.

## Functional Scope

### 1. Lesson Plans

Teachers should be able to:

- Create lesson plans.
- Update lesson plans.
- Copy existing lesson plans to speed up preparation.
- Connect one lesson plan to one or many students.
- Attach materials to lesson plans.

Materials may include:

- Images
- Audio files
- Other teaching files or references

### 2. Lessons

The system should support a separate lesson entity that can be shared with students online.

Teachers should be able to:

- Create lessons
- Update lessons
- Share lessons with students

Students should be able to:

- Open shared lessons online
- View lesson content and attached materials

### 3. Student Tracking

Teachers should be able to keep a structured history for each student.

This includes:

- Student profile or identity data
- Teacher notes
- Progress notes
- A view of all lessons related to a student

The student view should make it easy for a teacher to understand:

- What has already been covered
- How the student is progressing
- What lessons or plans are connected to that student

### 4. Schedule

Teachers should have a calendar-based scheduling view.

The schedule should allow teachers to:

- See upcoming lessons
- Manage lesson times
- View schedules connected to students
- See lesson readiness or status

Examples of useful statuses:

- Planned
- In preparation
- Ready
- Completed
- Cancelled

Exact status names can be refined later.

### 5. Authentication and Access

The app should support simple but reliable registration and authorization for teachers.

Teacher requirements:

- Register an account
- Log in securely
- Access only their own data

Student access requirements:

- Register and use the app as a regular user, or
- Access a lesson through a teacher-generated web link

Important constraint:

- Each generated link should be tied to a particular student

This helps preserve traceability and prevents fully anonymous open sharing by default.

### 6. Data Storage

All application data should be stored in a database.

Expected data domains include:

- Teachers
- Students
- Lesson plans
- Lessons
- Lesson materials
- Notes and progress records
- Schedules
- Shared lesson links
- Authentication-related records

The specific database technology is not yet defined in this document.

## Technical Direction

### Frontend

- React

### Backend

- Go

### Storage

- Database-backed persistence for all important entities

The final architecture, hosting model, and detailed stack choices can be refined later.

## Initial Domain Model Direction

The current idea suggests the following main entities:

- Teacher
- Student
- LessonPlan
- Lesson
- LessonMaterial
- StudentNote
- StudentProgressEntry
- ScheduleEvent
- ShareLink

Likely relationships:

- One teacher owns many students.
- One teacher owns many lesson plans.
- One lesson plan can be linked to one or many students.
- One lesson can reference one lesson plan or be created independently.
- One student can have many lessons.
- One lesson can have many materials.
- One share link belongs to one student and one lesson.

These relationships are a starting point and may evolve during implementation.

## Product Principles

The product should aim for:

- Reliability over unnecessary complexity
- Clear teacher workflows
- Fast access to lesson materials
- Secure handling of teacher and student data
- Good support for future incremental expansion

## Open Questions

The following points are intentionally left open for future planning:

- Exact authentication method and identity provider
- File storage strategy for uploaded materials
- Exact lesson and schedule status model
- Whether lesson plans and lessons should have strict or flexible separation
- How students authenticate when using invite or share links
- Notification strategy for teachers and students
- Multi-teacher support boundaries and tenancy model
- Deployment architecture for production

## Delivery Note

This business plan is the foundation for implementation planning, but it should not block practical iteration. As the product is built, the team may refine the domain model, workflows, and technical choices based on actual implementation feedback.
