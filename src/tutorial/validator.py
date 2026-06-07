import json
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
from .models import PlanTree, ValidationCriteria, ValidationResult
from .sandbox import SandboxInterface

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

class ExerciseValidator(ABC):
    """
    Exercise Validator (EV)
    Interface for evaluating user submissions against execution plan criteria.
    """

    @abstractmethod
    def get_execution_plan(self, sql: str, db_type: str) -> PlanTree:
        """
        Requests DSI to run EXPLAIN on the SQL and returns a structured plan tree.

        :param sql: User-provided SQL statement.
        :param db_type: Database type ('postgres' or 'oracle').
        :return: A structured PlanTree object.
        """
        pass

    @abstractmethod
    def validate(self, user_sql: str, criteria: ValidationCriteria) -> ValidationResult:
        """
        Runs validation by comparing the user's execution plan against the criteria.

        :param user_sql: User-provided SQL statement.
        :param criteria: Validation criteria defined in the exercise.
        :return: ValidationResult with success/failure and feedback.
        """
        pass

class DefaultExerciseValidator(ExerciseValidator):
    """
    Standard implementation of ExerciseValidator using recursive plan tree comparison.
    """

    def __init__(self, sandbox: Optional[SandboxInterface] = None):
        self.sandbox = sandbox
        self.pg_parser = PostgresPlanParser()

    def get_execution_plan(self, sql: str, db_type: str = "postgres") -> PlanTree:
        if not self.sandbox:
            raise RuntimeError("Validator not connected to a sandbox.")

        if db_type.lower() == "postgres":
            explain_sql = f"EXPLAIN (FORMAT JSON) {sql}"
            result = self.sandbox.execute_query(explain_sql)
            if result.error:
                raise RuntimeError(f"Error getting execution plan: {result.error}")

            # Postgres JSON output is usually in the first row, first column
            if result.rows and len(result.rows[0]) > 0:
                json_plan = result.rows[0][0]
                if isinstance(json_plan, (dict, list)):
                    json_plan = json.dumps(json_plan)
                return self.pg_parser.parse(json_plan)
            raise ValueError("No execution plan returned by the database.")
        else:
            raise NotImplementedError(f"Plan capture for '{db_type}' not supported yet.")

    def validate(self, user_sql: str, criteria: ValidationCriteria) -> ValidationResult:
        try:
            plan_tree = self.get_execution_plan(user_sql, criteria.db_type)
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
