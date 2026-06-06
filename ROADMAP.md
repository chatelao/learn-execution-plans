# ROADMAP.md - Execution Plan Mastery Tutorial

## Progress Overview

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Project Foundation | ✅ |
| Phase 2 | Infrastructure & CI/CD | ✅ |
| Phase 3 | Technical Interface Specifications | ✅ |
| Phase 4 | Database Sandbox Interface (DSI) | ⏳ |
| Phase 5 | Content Management & Lesson Engine | ⏳ |
| Phase 6 | Exercise Validator (EV) | ⏳ |
| Phase 7 | Web UI Development | ⏳ |
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
- [x] Define `tutorial.engine` internal interfaces ✅
- [x] Define `tutorial.sandbox` internal interfaces ✅
- [x] Define `tutorial.validator` internal interfaces ✅
- [x] Define Content Repository file structure and YAML schemas ✅

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

### Phase 7: Web UI Development
- [ ] Implement Web-based User Interface ⏳
- [ ] Create UI for lesson navigation ⏳
- [ ] Create UI for exercise submission ⏳
- [ ] Implement progress dashboard ⏳

### Phase 8: Content Production
- [ ] Produce Oracle execution plan constructs lessons ⏳
- [ ] Produce PostgreSQL execution plan constructs lessons ⏳
  - [ ] Lesson: Scan (ex_scan.svg) ⏳
  - [ ] Lesson: Index Scan (ex_index_scan.svg) ⏳
  - [ ] Lesson: Index Only Scan (ex_index_only_scan.svg) ⏳
  - [ ] Lesson: Nested (ex_nested.svg) ⏳
  - [ ] Lesson: Join (ex_join.svg) ⏳
  - [ ] Lesson: Hash (ex_hash.svg) ⏳
  - [ ] Lesson: Merge (ex_merge.svg) ⏳
  - [ ] Lesson: Bmp Index (ex_bmp_index.svg) ⏳
  - [ ] Lesson: Bmp Heap (ex_bmp_heap.svg) ⏳
  - [ ] Lesson: Bmp And (ex_bmp_and.svg) ⏳
  - [ ] Lesson: Bmp Or (ex_bmp_or.svg) ⏳
  - [ ] Lesson: Sort (ex_sort.svg) ⏳
  - [ ] Lesson: Aggregate (ex_aggregate.svg) ⏳
  - [ ] Lesson: Group (ex_group.svg) ⏳
  - [ ] Lesson: Unique (ex_unique.svg) ⏳
  - [ ] Lesson: Limit (ex_limit.svg) ⏳
  - [ ] Lesson: Insert (ex_insert.svg) ⏳
  - [ ] Lesson: Update (ex_update.svg) ⏳
  - [ ] Lesson: Delete (ex_delete.svg) ⏳
  - [ ] Lesson: Lock Rows (ex_lock_rows.svg) ⏳
  - [ ] Lesson: Materialize (ex_materialize.svg) ⏳
  - [ ] Lesson: Result (ex_result.svg) ⏳
  - [ ] Lesson: Cte Scan (ex_cte_scan.svg) ⏳
  - [ ] Lesson: Worktable Scan (ex_worktable_scan.svg) ⏳
  - [ ] Lesson: Subplan (ex_subplan.svg) ⏳
  - [ ] Lesson: Append (ex_append.svg) ⏳
  - [ ] Lesson: Merge Append (ex_merge_append.svg) ⏳
  - [ ] Lesson: Recursive Union (ex_recursive_union.svg) ⏳
  - [ ] Lesson: Nested Loop Semi Join (ex_nested_loop_semi_join.svg) ⏳
  - [ ] Lesson: Nested Loop Anti Join (ex_nested_loop_anti_join.svg) ⏳
  - [ ] Lesson: Hash Semi Join (ex_hash_semi_join.svg) ⏳
  - [ ] Lesson: Hash Anti Join (ex_hash_anti_join.svg) ⏳
  - [ ] Lesson: Merge Semi Join (ex_merge_semi_join.svg) ⏳
  - [ ] Lesson: Merge Anti Join (ex_merge_anti_join.svg) ⏳
  - [ ] Lesson: Gather Merge (ex_gather_merge.svg) ⏳
  - [ ] Lesson: Gather Motion (ex_gather_motion.svg) ⏳
  - [ ] Lesson: Window Aggregate (ex_window_aggregate.svg) ⏳
  - [ ] Lesson: Projectset (ex_projectset.svg) ⏳
  - [ ] Lesson: Foreign Scan (ex_foreign_scan.svg) ⏳
  - [ ] Lesson: Tid Scan (ex_tid_scan.svg) ⏳
  - [ ] Lesson: Values Scan (ex_values_scan.svg) ⏳
  - [ ] Lesson: Named Tuplestore Scan (ex_named_tuplestore_scan.svg) ⏳
  - [ ] Lesson: Table Func Scan (ex_table_func_scan.svg) ⏳
  - [ ] Lesson: Seek (ex_seek.svg) ⏳
  - [ ] Lesson: Setop (ex_setop.svg) ⏳
  - [ ] Lesson: Hash Setop Unknown (ex_hash_setop_unknown.svg) ⏳
  - [ ] Lesson: Hash Setop Except (ex_hash_setop_except.svg) ⏳
  - [ ] Lesson: Hash Setop Except All (ex_hash_setop_except_all.svg) ⏳
  - [ ] Lesson: Hash Setop Intersect (ex_hash_setop_intersect.svg) ⏳
  - [ ] Lesson: Hash Setop Intersect All (ex_hash_setop_intersect_all.svg) ⏳
  - [ ] Lesson: Citus (ex_citus.svg) ⏳
  - [ ] Lesson: Citus Worker Task (ex_citus_worker_task.svg) ⏳
  - [ ] Lesson: Citus Distributed One Of One (ex_citus_distributed_one_of_one.svg) ⏳
  - [ ] Lesson: Citus Distributed One Of Many (ex_citus_distributed_one_of_many.svg) ⏳
  - [ ] Lesson: Broadcast Motion (ex_broadcast_motion.svg) ⏳
  - [ ] Lesson: Redistribute Motion (ex_redistribute_motion.svg) ⏳
  - [ ] Lesson: Unknown (ex_unknown.svg) ⏳
- [ ] Create interactive optimization exercises ⏳
- [ ] Conduct knowledge verification test suites ⏳
