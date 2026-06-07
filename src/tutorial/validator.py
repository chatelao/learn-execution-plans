from abc import ABC, abstractmethod
from typing import Any, List, Dict
from .models import PlanTree, ValidationCriteria, ValidationResult

class ExerciseValidator(ABC):
    """
    Exercise Validator (EV)
    Interface for evaluating user submissions against execution plan criteria.
    """

    @abstractmethod
    def get_execution_plan(self, sql: str) -> PlanTree:
        """
        Requests DSI to run EXPLAIN on the SQL and returns a structured plan tree.

        :param sql: User-provided SQL statement.
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

    def get_execution_plan(self, sql: str) -> PlanTree:
        # This will be implemented when connected to the Database Sandbox
        raise NotImplementedError("get_execution_plan depends on a concrete Sandbox implementation.")

    def validate(self, user_sql: str, criteria: ValidationCriteria) -> ValidationResult:
        try:
            plan_tree = self.get_execution_plan(user_sql)
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
        """
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
