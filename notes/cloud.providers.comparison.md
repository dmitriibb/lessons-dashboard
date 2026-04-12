# Cloud Providers Comparison

## Purpose

This note captures the current comparison of small-instance cloud hosting options for Lessons Dashboard, with the focus narrowed to:

- `Google Cloud Compute Engine`
- `AWS EC2`

The comparison is based on the current intended early-stage deployment model:

- one `Go` backend
- one SQL database
- one `React` client application
- one reverse proxy
- one always-needed main environment
- occasional use of a second environment for `dev` or feature work

This document reflects the analysis discussed on April 12, 2026.

## Main Cost Preference

The preferred pricing model is not a flat monthly bundle. The preference is:

- pay mainly for actual runtime when instances are running
- keep costs low by stopping instances when they are not needed

Both Google Cloud and AWS support this model for VMs.

## Stop and Start Behavior

### Google Cloud

When a Compute Engine VM is stopped:

- CPU charges stop
- attached disks still cost money
- reserved external IPs can still cost money

This means Google Cloud works well if the app is needed only for a few hours and can stay off for long periods.

### AWS

When an EC2 instance is stopped:

- instance usage charges stop
- EBS storage still costs money
- some other attached resources may still cost money

This means AWS also supports the same basic stop-and-start cost model.

## Important Conclusion

Google Cloud is not unique in letting you save money by stopping instances. AWS can also do that.

However, for the small VM sizes relevant to this project, Google Cloud currently looks cheaper than AWS for comparable instance sizes.

## Instance Sizes and Memory

### Google Cloud E2 shared-core options

Relevant small machine types:

- `e2-micro` = `1 GiB RAM`
- `e2-small` = `2 GiB RAM`
- `e2-medium` = `4 GiB RAM`

### AWS T3 examples

Relevant small machine types:

- `t3.micro` = `1 GB RAM`
- `t3.small` = `2 GB RAM`
- `t3.medium` = `4 GB RAM`

These memory sizes are the key reference points for the current deployment planning.

## Estimated Memory Need for Our App

Assumed runtime components:

- Linux VM
- Docker
- reverse proxy
- Go API
- React client application
- database

### Approximate memory usage by component

- Linux + Docker + base services: `250-400 MB`
- reverse proxy: `30-80 MB`
- Go API: `60-150 MB` at light load, possibly more under real usage
- React client app:
  - if built and served as static assets, runtime memory cost is near zero outside the web server
  - if run as its own frontend container or process, it will need more memory than pure static hosting
- MySQL 8: often `350-700 MB` even when tuned small
- MariaDB: often `150-400 MB` when tuned for a small VM

### Practical totals

With `MariaDB`:

- expected light idle range: about `0.5-1.0 GB`
- practical working range with some usage: about `1.2-1.8 GB`

With `MySQL`:

- expected light idle range: about `0.7-1.3 GB`
- practical working range with some usage: about `1.5-2.2 GB`

## Memory Conclusion

- `2 GB RAM` is possible only with careful tuning and limited headroom
- `4 GB RAM` is the more practical minimum for a comfortable setup
- if main and dev ever run together on one machine, `4 GB` is much safer than `2 GB`

## Database Choice

The original idea mentioned `MySQL`, but a lighter database was requested if possible.

### Recommendation

Use `MariaDB` instead of `MySQL` for the early self-hosted setup.

Why:

- lighter memory footprint
- operationally familiar for a MySQL-like setup
- suitable for a small single-VM deployment

### Database ranking for this project stage

1. `MariaDB` as the preferred lightweight practical choice
2. `MySQL` as acceptable but heavier
3. `PostgreSQL` as strong technically, but not chosen here for the low-cost-memory target
4. `SQLite` as too limited for the intended multi-user hosted app

## Price Comparison

The prices below are rough estimates based on the provider documentation discussed during analysis.

Assumptions:

- one VM
- one local database on that VM
- `50 GB` disk
- one public IPv4
- low traffic
- no object storage, email, CDN, or advanced backups included

### Google Cloud

Approximate pricing in a low-cost region such as `us-central1`:

- `e2-small`:
  - `2 GiB RAM`
  - about `$0.016752855/hour`
- `e2-medium`:
  - `4 GiB RAM`
  - about `$0.03350571/hour`

Approximate disk cost:

- `50 GB` standard persistent disk = about `$2/month`

Approximate external IPv4 cost:

- about `$0.005/hour`

#### Always-on estimate

- `e2-small`:
  - compute about `$12.23/month`
  - disk about `$2.00/month`
  - IPv4 about `$3.65/month`
  - total about `$17.88/month`
- `e2-medium`:
  - compute about `$24.46/month`
  - disk about `$2.00/month`
  - IPv4 about `$3.65/month`
  - total about `$30.11/month`

#### Part-time estimate

If the app runs about `10 hours`, then remains off for about `2 days`, the monthly running time is roughly `125.9 hours`.

- `e2-small`:
  - compute about `$2.11/month`
  - disk about `$2.00/month`
  - IPv4 during running time about `$0.63/month`
  - total about `$4.74/month`
- `e2-medium`:
  - compute about `$4.22/month`
  - disk about `$2.00/month`
  - IPv4 about `$0.63/month`
  - total about `$6.85/month`

### AWS EC2

Approximate pricing in `us-east-1`:

- `t3.small`:
  - `2 GB RAM`
  - about `$0.0208/hour`
- `t3.medium`:
  - `4 GB RAM`
  - about `$0.0416/hour`

Approximate disk cost:

- `50 GB` `gp3` EBS = about `$4/month`

Approximate public IPv4 cost:

- about `$0.005/hour`

#### Always-on estimate

- `t3.small`:
  - compute about `$15.18/month`
  - disk about `$4.00/month`
  - IPv4 about `$3.65/month`
  - total about `$22.83/month`
- `t3.medium`:
  - compute about `$30.37/month`
  - disk about `$4.00/month`
  - IPv4 about `$3.65/month`
  - total about `$38.02/month`

#### Part-time estimate

Using the same `125.9` running hours per month:

- `t3.small`:
  - compute about `$2.62/month`
  - disk about `$4.00/month`
  - IPv4 about `$0.63/month`
  - total about `$7.25/month`
- `t3.medium`:
  - compute about `$5.24/month`
  - disk about `$4.00/month`
  - IPv4 about `$0.63/month`
  - total about `$9.87/month`

## Practical Comparison Summary

### Google Cloud strengths

- cheaper than AWS in the compared small sizes
- lower persistent disk cost in this comparison
- stop-and-start model fits the desired usage pattern
- straightforward choice for a low-cost single-VM setup

### AWS strengths

- also supports stop-and-start savings
- strong ecosystem and future growth options

### AWS caution

The AWS pricing model for burstable instances can be less predictable because of CPU credit behavior in some configurations. That is not ideal for the current goal of simple and cheap hosting.

## Chosen Direction

Based on the comparison, the preferred infrastructure choice is:

- `Google Cloud Compute Engine`
- `e2-medium`
- `4 GiB RAM`
- `MariaDB`

The agreed deployment design is documented in:

- [docs/infra/cloud.deployment.md](/c:/projects/lessons-dashboard/docs/infra/cloud.deployment.md)

## Sources

Primary sources used during the comparison:

- Google Compute general-purpose machine types: https://cloud.google.com/compute/docs/general-purpose-machines
- Google Compute pricing: https://cloud.google.com/compute/all-pricing?hl=en
- Google persistent disk pricing: https://cloud.google.com/compute/disks-image-pricing
- Google stop and suspend pricing behavior: https://cloud.google.com/compute/docs/instances/suspend-stop-reset-instances-overview
- Google external IP pricing: https://cloud.google.com/vpc/pricing-announce-external-ips
- AWS EC2 instance lifecycle billing: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html
- AWS EC2 on-demand pricing: https://aws.amazon.com/ec2/pricing/on-demand/
- AWS T3 size and hourly examples: https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html
- AWS EBS pricing: https://aws.amazon.com/ebs/pricing/
- AWS public IPv4 pricing: https://aws.amazon.com/en/vpc/pricing/
