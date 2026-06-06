# ROADMAP.md - Execution Plan Mastery Tutorial

## Progress Overview

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Project Foundation | ✅ |
| Phase 2 | Infrastructure & CI/CD | ✅ |
| Phase 3 | Technical Interface Specifications | ⏳ |
| Phase 4 | Database Sandbox Interface (DSI) | ⏳ |
| Phase 5 | Content Management & Lesson Engine | ⏳ |
| Phase 6 | Exercise Validator (EV) | ⏳ |
| Phase 7 | CLI Development | ⏳ |
| Phase 8 | Content Production | ⏳ |

## Goals

- Build a step-by-step tutorial for Oracle and PostgreSQL execution plans ✅
- Provide certifiable knowledge for DBAs and developers ⏳
- Deliver interactive optimization exercises with immediate feedback ⏳
- Support local execution via Docker for isolation and fidelity ⏳
- Use a transparent YAML + Markdown content format ⏳

## Phases

### Phase 1: Project Foundation
- [x] Define business and use cases in `CONCEPT.md` ✅
- [x] Establish high-level functional architecture ✅
- [x] Define technical stack and detailed architecture in `DESIGN.md` ✅
- [x] Create top-level architecture diagram (`TOP_ARCHITECTURE.puml`) ✅
- [/] Create and maintain `ROADMAP.md` 🚧

### Phase 2: Infrastructure & CI/CD
- [x] Setup `src/install.sh` for build tools ✅
- [x] Setup `test/install.sh` for test tools ✅
- [x] Configure GitHub Action Workflows for CI/CD ✅
- [x] Setup ReadTheDocs documentation publishing ✅
- [x] Implement empty CI/CD pipeline ✅

### Phase 3: Technical Interface Specifications
- [ ] Define `tutorial.engine` internal interfaces ⏳
- [ ] Define `tutorial.sandbox` internal interfaces ⏳
- [ ] Define `tutorial.validator` internal interfaces ⏳
- [ ] Define Content Repository file structure and YAML schemas ⏳

### Phase 4: Database Sandbox Interface (DSI)
- [ ] Implement Docker management using Docker SDK for Python ⏳
- [ ] Create pre-configured Docker images for Oracle ⏳
- [ ] Create pre-configured Docker images for PostgreSQL ⏳
- [ ] Implement SQL execution and result capture logic ⏳

### Phase 5: Content Management & Lesson Engine
- [ ] Implement `tutorial.engine` for curriculum management ⏳
- [ ] Implement user progress tracking (JSON/SQLite) ⏳
- [ ] Implement `tutorial.content` for loading Markdown and YAML ⏳
- [ ] Create initial lesson templates ⏳

### Phase 6: Exercise Validator (EV)
- [ ] Implement execution plan capture (`EXPLAIN`) for Oracle ⏳
- [ ] Implement execution plan capture (`EXPLAIN`) for PostgreSQL ⏳
- [ ] Implement plan tree parsing and comparison logic ⏳
- [ ] Implement validation feedback generator ⏳

### Phase 7: CLI Development
- [ ] Implement Typer-based CLI framework ⏳
- [ ] Create commands for lesson navigation (`list`, `start`, `next`) ⏳
- [ ] Create commands for exercise submission (`submit`, `hint`) ⏳
- [ ] Implement progress reporting commands ⏳

### Phase 8: Content Production
- [ ] Produce Oracle execution plan constructs lessons ⏳
- [ ] Produce PostgreSQL execution plan constructs lessons ⏳
- [ ] Create interactive optimization exercises ⏳
- [ ] Conduct knowledge verification test suites ⏳
