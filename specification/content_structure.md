# Content Repository Structure and Schemas

This document defines the file system layout and YAML schemas for the educational content (lessons and exercises) used by the Execution Plan Mastery Tutorial.

## Directory Structure

The content is stored in a `content/` directory at the repository root, organized as follows:

```text
content/
├── lessons/
│   ├── L01_intro_to_plans/
│   │   ├── lesson.md
│   │   └── metadata.yaml
│   └── L02_scans/
│       ├── lesson.md
│       └── metadata.yaml
└── exercises/
    ├── E01_simple_scan/
    │   ├── setup.sql
    │   ├── validation.yaml
    │   └── metadata.yaml
    └── E02_index_usage/
        ├── setup.sql
        ├── validation.yaml
        └── metadata.yaml
```

## Schemas

### Lesson Metadata (`lessons/*/metadata.yaml`)

```yaml
id: L01_intro_to_plans
title: "Introduction to Execution Plans"
order: 1
tags: ["basics", "concepts"]
prerequisites: []
```

### Exercise Metadata (`exercises/*/metadata.yaml`)

```yaml
id: E01_simple_scan
title: "A Simple Full Table Scan"
lesson_id: L02_scans
difficulty: "beginner"
```

### Exercise Validation (`exercises/*/validation.yaml`)

```yaml
expected_constructs:
  - operation: "TABLE ACCESS"
    options: "FULL"
forbidden_constructs:
  - operation: "INDEX"
custom_rules:
  min_cost: 0
  max_rows: 100
```

## Lesson Content (`lessons/*/lesson.md`)

Lesson files use standard Markdown with support for:
- Code blocks (SQL, execution plans)
- Images (locally stored or external)
- Callouts for tips and warnings
