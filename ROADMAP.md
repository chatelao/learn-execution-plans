# ROADMAP.md - Execution Plan Mastery Tutorial

## Progress Overview

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Project Foundation | ✅ |
| Phase 2 | Infrastructure & CI/CD | ✅ |
| Phase 3 | Technical Interface Specifications | ✅ |
| Phase 4 | Database Sandbox Interface (DSI) | ⏳ |
| Phase 5 | Content Management & Lesson Engine | ✅ |
| Phase 6 | Exercise Validator (EV) | ⏳ |
| Phase 7 | Web UI Development | ⏳ |
| Phase 8 | Content Production | 🚧 |

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
- [x] Implement `tutorial.engine` for curriculum management ✅ (2024-05-22)
- [x] Implement user progress tracking (JSON/SQLite) ✅ (2024-05-22)
- [x] Implement `tutorial.content` for loading Markdown and YAML ✅
- [x] Create initial lesson templates ✅ (2024-05-22)

### Phase 6: Exercise Validator (EV)
- [ ] Implement execution plan capture (`EXPLAIN`) for Oracle ⏳
- [x] Implement execution plan capture (`EXPLAIN`) for PostgreSQL ✅ (2024-05-22)
- [x] Implement plan tree parsing and comparison logic ✅ (2024-05-22)
- [ ] Implement validation feedback generator ⏳

### Phase 7: Web UI Development
- [ ] Implement Web-based User Interface ⏳
- [ ] Create UI for lesson navigation ⏳
- [ ] Create UI for exercise submission ⏳
- [ ] Implement progress dashboard ⏳

### Phase 8: Content Production
- [ ] Produce Oracle execution plan constructs lessons ⏳
  - [ ] Lesson: Table Access Full ⏳
  - [ ] Lesson: Index Unique Scan ⏳
  - [ ] Lesson: Index Range Scan ⏳
  - [ ] Lesson: Index Full Scan ⏳
  - [ ] Lesson: Index Fast Full Scan ⏳
  - [ ] Lesson: Index Skip Scan ⏳
  - [ ] Lesson: Table Access By Index Rowid ⏳
  - [ ] Lesson: Nested Loops ⏳
  - [ ] Lesson: Hash Join ⏳
  - [ ] Lesson: Merge Join ⏳
  - [ ] Lesson: Sort Aggregate ⏳
  - [ ] Lesson: Hash Unique ⏳
  - [ ] Lesson: View ⏳
  - [ ] Lesson: Union-All ⏳
  - [ ] Lesson: Filter ⏳
  - [ ] Lesson: Bitmap Index Operations ⏳
  - [ ] Lesson: Partitioning Operations ⏳
  - [ ] Lesson: Window Functions ⏳
  - [ ] Lesson: Hierarchical Queries (Connect By) ⏳
- [x] Produce PostgreSQL execution plan constructs lessons ✅ (2026-06-06)
  - [x] Lesson: Scan (ex_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Index Scan (ex_index_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Index Only Scan (ex_index_only_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Nested (ex_nested.svg) ✅ (2026-06-06)
  - [x] Lesson: Join (ex_join.svg) ✅ (2026-06-06)
  - [x] Lesson: Hash (ex_hash.svg) ✅ (2026-06-06)
  - [x] Lesson: Merge (ex_merge.svg) ✅ (2026-06-06)
  - [x] Lesson: Bmp Index (ex_bmp_index.svg) ✅ (2026-06-06)
  - [x] Lesson: Bmp Heap (ex_bmp_heap.svg) ✅ (2026-06-06)
  - [x] Lesson: Bmp And (ex_bmp_and.svg) ✅ (2026-06-06)
  - [x] Lesson: Bmp Or (ex_bmp_or.svg) ✅ (2026-06-06)
  - [x] Lesson: Sort (ex_sort.svg) ✅ (2026-06-06)
  - [x] Lesson: Aggregate (ex_aggregate.svg) ✅ (2026-06-06)
  - [x] Lesson: Group (ex_group.svg) ✅ (2026-06-06)
  - [x] Lesson: Unique (ex_unique.svg) ✅ (2026-06-06)
  - [x] Lesson: Limit (ex_limit.svg) ✅ (2026-06-06)
  - [x] Lesson: Insert (ex_insert.svg) ✅ (2026-06-06)
  - [x] Lesson: Update (ex_update.svg) ✅ (2026-06-06)
  - [x] Lesson: Delete (ex_delete.svg) ✅ (2026-06-06)
  - [x] Lesson: Lock Rows (ex_lock_rows.svg) ✅ (2026-06-06)
  - [x] Lesson: Materialize (ex_materialize.svg) ✅ (2026-06-06)
  - [x] Lesson: Result (ex_result.svg) ✅ (2026-06-06)
  - [x] Lesson: Cte Scan (ex_cte_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Worktable Scan (ex_worktable_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Subplan (ex_subplan.svg) ✅ (2026-06-06)
  - [x] Lesson: Append (ex_append.svg) ✅ (2026-06-06)
  - [x] Lesson: Merge Append (ex_merge_append.svg) ✅ (2026-06-06)
  - [x] Lesson: Recursive Union (ex_recursive_union.svg) ✅ (2026-06-06)
  - [x] Lesson: Nested Loop Semi Join (ex_nested_loop_semi_join.svg) ✅ (2026-06-06)
  - [x] Lesson: Nested Loop Anti Join (ex_nested_loop_anti_join.svg) ✅ (2026-06-06)
  - [x] Lesson: Hash Semi Join (ex_hash_semi_join.svg) ✅ (2026-06-06)
  - [x] Lesson: Hash Anti Join (ex_hash_anti_join.svg) ✅ (2026-06-06)
  - [x] Lesson: Merge Semi Join (ex_merge_semi_join.svg) ✅ (2026-06-06)
  - [x] Lesson: Merge Anti Join (ex_merge_anti_join.svg) ✅ (2026-06-06)
  - [x] Lesson: Gather Merge (ex_gather_merge.svg) ✅ (2026-06-06)
  - [x] Lesson: Gather Motion (ex_gather_motion.svg) ✅ (2026-06-06)
  - [x] Lesson: Window Aggregate (ex_window_aggregate.svg) ✅ (2026-06-06)
  - [x] Lesson: Projectset (ex_projectset.svg) ✅ (2026-06-06)
  - [x] Lesson: Foreign Scan (ex_foreign_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Tid Scan (ex_tid_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Values Scan (ex_values_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Named Tuplestore Scan (ex_named_tuplestore_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Table Func Scan (ex_table_func_scan.svg) ✅ (2026-06-06)
  - [x] Lesson: Seek (ex_seek.svg) ✅ (2026-06-06)
  - [x] Lesson: Setop (ex_setop.svg) ✅ (2026-06-06)
  - [x] Lesson: Hash Setop Unknown (ex_hash_setop_unknown.svg) ✅ (2026-06-06)
  - [x] Lesson: Hash Setop Except (ex_hash_setop_except.svg) ✅ (2026-06-06)
  - [x] Lesson: Hash Setop Except All (ex_hash_setop_except_all.svg) ✅ (2026-06-06)
  - [x] Lesson: Hash Setop Intersect (ex_hash_setop_intersect.svg) ✅ (2026-06-06)
  - [x] Lesson: Hash Setop Intersect All (ex_hash_setop_intersect_all.svg) ✅ (2026-06-06)
  - [x] Lesson: Citus (ex_citus.svg) ✅ (2026-06-06)
  - [x] Lesson: Citus Worker Task (ex_citus_worker_task.svg) ✅ (2026-06-06)
  - [x] Lesson: Citus Distributed One Of One (ex_citus_distributed_one_of_one.svg) ✅ (2026-06-06)
  - [x] Lesson: Citus Distributed One Of Many (ex_citus_distributed_one_of_many.svg) ✅ (2026-06-06)
  - [x] Lesson: Broadcast Motion (ex_broadcast_motion.svg) ✅ (2026-06-06)
  - [x] Lesson: Redistribute Motion (ex_redistribute_motion.svg) ✅ (2026-06-06)
  - [x] Lesson: Unknown (ex_unknown.svg) ✅ (2026-06-06)
- [/] Create interactive optimization exercises 🚧 (PostgreSQL Index Scan lesson and exercise added)
- [ ] Conduct knowledge verification test suites ⏳
