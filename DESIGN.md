# DESIGN.md - Execution Plan Mastery Tutorial

## Technical Stack
- **Language**: Python 3.10+
- **CLI Framework**: Typer
- **Docker Management**: Docker SDK for Python
- **Database Connectivity**: `cx_Oracle` (Oracle), `psycopg2` (PostgreSQL)
- **Serialization**: PyYAML for lesson and exercise metadata
- **Documentation**: Sphinx / ReadTheDocs

## Detailed Architecture

### 1. Lesson Engine (LE)
The core logic that orchestrates the learning flow.
- **Responsibility**: Tracks user progress (local JSON/SQLite), loads content from the Content Repository, and coordinates with the Sandbox and Validator.
- **Technical Interface**: Internal Python module `tutorial.engine`.

### 2. Database Sandbox Interface (DSI)
A wrapper around Docker to manage database lifecycles.
- **Responsibility**: Provisioning and tearing down Oracle and PostgreSQL containers. Executing user-provided SQL scripts within these containers.
- **Technical Interface**: Internal Python module `tutorial.sandbox`, using the Docker SDK for Python.

### 3. Exercise Validator (EV)
The evaluation logic for user submissions.
- **Responsibility**: Captures the execution plan of a user's SQL statement using `EXPLAIN PLAN` (Oracle) or `EXPLAIN` (PostgreSQL), parses the resulting tree, and compares it against the expected constructs defined in the exercise.
- **Technical Interface**: Internal Python module `tutorial.validator`.

### 4. Content Repository (CR)
The storage for all educational material.
- **Responsibility**: Holds lesson text (Markdown), schema setup scripts (SQL), and exercise validation rules (YAML).
- **Technical Interface**: File system structure under `content/`.

## Top-Level Architecture
![TOP_ARCHITECTURE](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/user/repo/main/TOP_ARCHITECTURE.puml)

*Note: The above URL is a placeholder for dynamic rendering of `TOP_ARCHITECTURE.puml` once pushed to the repository.*

## Technical Interfaces

### LE <-> DSI
- `DSI.setup_environment(db_type: str, init_sql: str)`: Prepares the container with the required schema.
- `DSI.execute_query(sql: str) -> QueryResult`: Executes a query and returns results.

### LE <-> CR
- `CR.get_lesson(lesson_id: str) -> LessonData`: Loads markdown and metadata for a lesson.
- `CR.get_exercise(exercise_id: str) -> ExerciseData`: Loads validation rules and setup scripts.

### EV <-> DSI
- `EV.get_execution_plan(sql: str) -> PlanTree`: Requests DSI to run `EXPLAIN` on the SQL and returns a structured plan.

### LE <-> EV
- `EV.validate(user_sql: str, criteria: ValidationCriteria) -> ValidationResult`: Runs validation and returns success/failure with feedback.

## Major Choices

### Choice 1: Implementation Language & Framework
- **Alternative 1: Python with Typer**
  - *Pros*: Excellent library support for database interaction and Docker; low barrier to entry for scripting; Typer provides a modern, type-hinted CLI experience.
  - *Cons*: Slower execution compared to compiled languages (negligible for this use case).
- **Alternative 2: Node.js with oclif**
  - *Pros*: Strong ecosystem for CLI tools; good async support.
  - *Cons*: Managing local Docker containers and complex DB drivers (especially Oracle) can be more cumbersome than in Python.
- **Alternative 3: Go with Cobra**
  - *Pros*: Fast, single-binary distribution; excellent Docker integration.
  - *Cons*: Steeper learning curve for content contributors; less flexible for the rapid development of educational logic.

**Chosen Alternative: Alternative 1 - Python with Typer.**
Python's balance of readability and powerful libraries for database and system management makes it ideal for a tutorial system that may be extended by database professionals.

### Choice 2: User Interface Type
- **Alternative 1: Command-Line Interface (CLI)**
  - *Pros*: Directly aligns with the workflow of DBAs and developers; easy to automate; minimal overhead.
  - *Cons*: Steep learning curve for non-technical users (not our target audience).
- **Alternative 2: Web-based GUI (SPA)**
  - *Pros*: More visual; lower barrier to entry.
  - *Cons*: Complex to manage local Docker containers from a browser (requires a local proxy or heavy backend); higher development effort.
- **Alternative 3: VS Code Extension**
  - *Pros*: Integrated directly into the IDE where users write SQL.
  - *Cons*: Ties the user to a specific editor.

**Chosen Alternative: Alternative 1 - Command-Line Interface (CLI).**
A CLI tool provides the most direct and realistic experience for users aiming for professional database certification.

### Choice 3: Content Metadata Format
- **Alternative 1: YAML + Markdown Files**
  - *Pros*: Human-readable; version-controllable; easy for contributors to edit.
  - *Cons*: Requires file system parsing logic.
- **Alternative 2: Embedded SQLite Database**
  - *Pros*: Easy to query; relational integrity.
  - *Cons*: Harder to version control changes to individual lessons; requires specialized tools to edit.
- **Alternative 3: Single JSON file**
  - *Pros*: Simple to parse.
  - *Cons*: Becomes unmanageable as content grows; hard to read and edit manually.

**Chosen Alternative: Alternative 1 - YAML + Markdown Files.**
This approach ensures that the tutorial content is as transparent and maintainable as the code itself.
