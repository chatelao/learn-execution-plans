import json
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
from .models import PlanTree, ValidationCriteria, ValidationResult

class PostgresPlanParser:
    """
    Parser for PostgreSQL EXPLAIN (FORMAT JSON) output.
    """

    def parse(self, json_output: str) -> PlanTree:
        try:
            data = json.loads(json_output)
            # PostgreSQL returns a list of queries; usually we just want the first one
            if isinstance(data, list) and len(data) > 0:
                plan_data = data[0].get("Plan", {})
                return self._parse_node(plan_data)
            raise ValueError("Invalid PostgreSQL EXPLAIN JSON format")
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON output: {str(e)}")

    def _parse_node(self, node_data: Dict[str, Any]) -> PlanTree:
        operation = node_data.get("Node Type", "UNKNOWN")
        children = []

        if "Plans" in node_data:
            for child_data in node_data["Plans"]:
                children.append(self._parse_node(child_data))

        # Collect all other fields as options
        options = {k: v for k, v in node_data.items() if k not in ("Node Type", "Plans")}

        return PlanTree(operation=operation, children=children, options=options)

from .sandbox import SandboxInterface

class ExerciseValidator(ABC):
    """
    Exercise Validator (EV)
    Interface for evaluating user submissions against execution plan criteria.
    """

    @abstractmethod
    def get_execution_plan(self, sql: str, sandbox: SandboxInterface) -> PlanTree:
        """
        Requests DSI to run EXPLAIN on the SQL and returns a structured plan tree.

        :param sql: User-provided SQL statement.
        :param sandbox: The database sandbox to use.
        :return: A structured PlanTree object.
        """
        pass

    @abstractmethod
    def validate(self, user_sql: str, criteria: ValidationCriteria, sandbox: SandboxInterface) -> ValidationResult:
        """
        Runs validation by comparing the user's execution plan against the criteria.

        :param user_sql: User-provided SQL statement.
        :param criteria: Validation criteria defined in the exercise.
        :param sandbox: The database sandbox to use.
        :return: ValidationResult with success/failure and feedback.
        """
        pass

class DefaultExerciseValidator(ExerciseValidator):
    """
    Standard implementation of ExerciseValidator using recursive plan tree comparison.
    """

    @abstractmethod
    def get_execution_plan(self, sql: str, sandbox: SandboxInterface) -> PlanTree:
        pass

    def validate(self, user_sql: str, criteria: ValidationCriteria, sandbox: SandboxInterface) -> ValidationResult:
        try:
            plan_tree = self.get_execution_plan(user_sql, sandbox)
        except Exception as e:
            return ValidationResult(success=False, feedback=f"Failed to capture execution plan: {str(e)}")

        # Check for forbidden constructs
        for forbidden in criteria.forbidden_constructs:
            if self._find_construct(plan_tree, forbidden):
                return ValidationResult(
                    success=False,
                    feedback=f"Forbidden construct found: {forbidden}",
                    plan_tree=plan_tree
                )

        # Check for expected constructs
        missing = []
        for expected in criteria.expected_constructs:
            if not self._find_construct(plan_tree, expected):
                missing.append(str(expected))

        if missing:
            return ValidationResult(
                success=False,
                feedback=f"Missing expected constructs: {', '.join(missing)}",
                plan_tree=plan_tree
            )

        return ValidationResult(success=True, feedback="Exercise validated successfully!", plan_tree=plan_tree)

    def _find_construct(self, tree: PlanTree, construct: Any) -> bool:
        """
        Recursively searches the plan tree for a matching construct.
        If construct is a list, it returns True if ANY item in the list matches (OR logic).
        """
        if isinstance(construct, list):
            return any(self._find_construct(tree, c) for c in construct)

        if self._matches(tree, construct):
            return True

        for child in tree.children:
            if self._find_construct(child, construct):
                return True

        return False

    def _matches(self, node: PlanTree, construct: Any) -> bool:
        """
        Checks if a plan tree node matches a construct definition.
        A construct can be a string (matching the operation) or a dictionary
        specifying multiple fields (operation, options, etc.).
        """
        if isinstance(construct, str):
            return node.operation.upper() == construct.upper()

        if isinstance(construct, dict):
            # All keys in the construct dictionary must match the node's attributes or options
            for key, value in construct.items():
                matched_key = None
                if hasattr(node, key):
                    matched_key = key
                    attr_val = getattr(node, key)
                else:
                    # Check options (case-insensitive key match)
                    for opt_key in node.options:
                        if opt_key.lower() == key.lower():
                            matched_key = opt_key
                            attr_val = node.options[opt_key]
                            break

                if matched_key is None:
                    return False

                # Compare values (case-insensitive if both are strings)
                if isinstance(attr_val, str) and isinstance(value, str):
                    if attr_val.upper() != value.upper():
                        return False
                elif attr_val != value:
                    return False

            return True

        return False

class OraclePlanParser:
    """
    Parser for Oracle EXPLAIN PLAN output retrieved from PLAN_TABLE.
    Expects a list of rows representing the plan steps.
    """

    def parse(self, rows: List[Dict[str, Any]]) -> PlanTree:
        if not rows:
            raise ValueError("No plan data to parse")

        # Build a map of ID -> Node and ID -> Children IDs
        nodes = {}
        children_map = {}
        root_id = None

        for row in rows:
            node_id = row.get("ID")
            parent_id = row.get("PARENT_ID")
            operation = row.get("OPERATION", "UNKNOWN")
            options = {k: v for k, v in row.items() if k not in ("ID", "PARENT_ID", "OPERATION")}

            node = PlanTree(operation=operation, children=[], options=options)
            nodes[node_id] = node

            if parent_id is None or parent_id == -1: # Oracle usually uses -1 or NULL for root parent
                root_id = node_id
            else:
                if parent_id not in children_map:
                    children_map[parent_id] = []
                children_map[parent_id].append(node_id)

        if root_id is None:
            # Fallback to the first node if no root is explicitly found
            root_id = rows[0].get("ID")

        # Recursively assemble the tree
        return self._assemble_tree(root_id, nodes, children_map)

    def _assemble_tree(self, node_id: int, nodes: Dict[int, PlanTree], children_map: Dict[int, List[int]]) -> PlanTree:
        node = nodes[node_id]
        if node_id in children_map:
            for child_id in sorted(children_map[node_id]):
                node.children.append(self._assemble_tree(child_id, nodes, children_map))
        return node

class PostgresExerciseValidator(DefaultExerciseValidator):
    """
    PostgreSQL-specific Exercise Validator.
    """

    def __init__(self):
        self.parser = PostgresPlanParser()

    def get_execution_plan(self, sql: str, sandbox: SandboxInterface) -> PlanTree:
        explain_sql = f"EXPLAIN (FORMAT JSON) {sql}"
        result = sandbox.execute_query(explain_sql)

        if result.error:
            raise ValueError(f"PostgreSQL error: {result.error}")

        # The result of EXPLAIN (FORMAT JSON) is typically a single row with one column containing the JSON string
        if not result.rows or not result.rows[0]:
            raise ValueError("No execution plan returned from PostgreSQL")

        plan_json = result.rows[0][0]
        # If it's already a dict/list (psycopg2 sometimes parses JSON automatically), convert it back to string or handle it
        if not isinstance(plan_json, str):
            plan_json = json.dumps(plan_json)

        return self.parser.parse(plan_json)

class OracleExerciseValidator(DefaultExerciseValidator):
    """
    Oracle-specific Exercise Validator.
    """

    def __init__(self):
        self.parser = OraclePlanParser()

    def get_execution_plan(self, sql: str, sandbox: SandboxInterface) -> PlanTree:
        # 1. Clear PLAN_TABLE for the current session (optional but good practice)
        sandbox.execute_query("DELETE FROM PLAN_TABLE")

        # 2. Run EXPLAIN PLAN
        explain_sql = f"EXPLAIN PLAN FOR {sql}"
        result = sandbox.execute_query(explain_sql)
        if result.error:
            raise ValueError(f"Oracle EXPLAIN PLAN error: {result.error}")

        # 3. Retrieve plan from PLAN_TABLE
        query = "SELECT id, parent_id, operation, options, object_name FROM PLAN_TABLE ORDER BY id"
        plan_result = sandbox.execute_query(query)

        if plan_result.error:
            raise ValueError(f"Failed to retrieve plan from PLAN_TABLE: {plan_result.error}")

        if not plan_result.rows:
            raise ValueError("No execution plan returned from Oracle")

        # Convert rows to list of dicts for the parser
        rows = []
        for r in plan_result.rows:
            rows.append({
                "ID": r[0],
                "PARENT_ID": r[1],
                "OPERATION": r[2],
                "OPTIONS": r[3],
                "OBJECT_NAME": r[4]
            })

        return self.parser.parse(rows)
