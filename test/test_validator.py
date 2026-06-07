import pytest
from unittest.mock import MagicMock
from tutorial.validator import DefaultExerciseValidator, PostgresPlanParser
from tutorial.models import PlanTree, ValidationCriteria, QueryResult

class MockValidator(DefaultExerciseValidator):
    def __init__(self, plan_to_return):
        # Override init to not require a sandbox for these simple tests
        self.plan_to_return = plan_to_return

    def get_execution_plan(self, sql: str) -> PlanTree:
        return self.plan_to_return

def test_validator_get_execution_plan_integration():
    # Test that DefaultExerciseValidator.get_execution_plan correctly uses the sandbox
    mock_sandbox = MagicMock()
    # Mocking EXPLAIN (FORMAT JSON) output
    pg_json = '[{"Plan": {"Node Type": "Seq Scan", "Relation Name": "users"}}]'
    mock_sandbox.execute_query.return_value = QueryResult(
        columns=["QUERY PLAN"],
        rows=[(pg_json,)],
        execution_time=0.1
    )

    validator = DefaultExerciseValidator(mock_sandbox)
    plan = validator.get_execution_plan("SELECT * FROM users")

    assert plan.operation == "Seq Scan"
    assert plan.options["Relation Name"] == "users"
    mock_sandbox.execute_query.assert_called_once_with("EXPLAIN (FORMAT JSON) SELECT * FROM users")

def test_validation_success_simple():
    # Setup a simple plan tree: TABLE ACCESS FULL
    plan = PlanTree(operation="TABLE ACCESS", options={"type": "FULL"})
    validator = MockValidator(plan)

    # Success case: expected operation
    criteria = ValidationCriteria(expected_constructs=["TABLE ACCESS"])
    result = validator.validate("SELECT * FROM table", criteria)
    assert result.success is True
    assert "successfully" in result.feedback

def test_validation_success_complex_match():
    plan = PlanTree(operation="TABLE ACCESS", options={"type": "FULL"})
    validator = MockValidator(plan)

    # Success case: matching operation and options
    criteria = ValidationCriteria(expected_constructs=[{"operation": "TABLE ACCESS", "type": "FULL"}])
    result = validator.validate("SELECT * FROM table", criteria)
    assert result.success is True

def test_validation_failure_missing_construct():
    plan = PlanTree(operation="TABLE ACCESS", options={"type": "FULL"})
    validator = MockValidator(plan)

    # Failure case: missing INDEX SCAN
    criteria = ValidationCriteria(expected_constructs=["INDEX SCAN"])
    result = validator.validate("SELECT * FROM table", criteria)
    assert result.success is False
    assert "Missing expected constructs" in result.feedback

def test_validation_failure_forbidden_construct():
    # Plan with a SORT operation
    plan = PlanTree(operation="SELECT STATEMENT", children=[
        PlanTree(operation="SORT", children=[
            PlanTree(operation="TABLE ACCESS")
        ])
    ])
    validator = MockValidator(plan)

    # Failure case: SORT is forbidden
    criteria = ValidationCriteria(expected_constructs=["TABLE ACCESS"], forbidden_constructs=["SORT"])
    result = validator.validate("SELECT * FROM table ORDER BY 1", criteria)
    assert result.success is False
    assert "Forbidden construct found: SORT" in result.feedback

def test_validation_recursive_matching():
    # Nested plan tree
    plan = PlanTree(operation="NESTED LOOPS", children=[
        PlanTree(operation="INDEX SCAN"),
        PlanTree(operation="TABLE ACCESS", options={"type": "BY INDEX ROWID"})
    ])
    validator = MockValidator(plan)

    # Check if it finds constructs deep in the tree
    criteria = ValidationCriteria(expected_constructs=[
        "INDEX SCAN",
        {"operation": "TABLE ACCESS", "type": "BY INDEX ROWID"}
    ])
    result = validator.validate("SELECT ...", criteria)
    assert result.success is True

def test_validation_case_insensitivity():
    plan = PlanTree(operation="Table Access", options={"Type": "Full"})
    validator = MockValidator(plan)

    criteria = ValidationCriteria(expected_constructs=[{"operation": "TABLE ACCESS", "type": "FULL"}])
    result = validator.validate("SELECT ...", criteria)
    assert result.success is True

def test_validation_or_logic():
    # Test Seq Scan (Postgres)
    plan_pg = PlanTree(operation="Seq Scan", options={"Relation Name": "users"})
    validator_pg = MockValidator(plan_pg)

    # Test Table Access Full (Oracle)
    plan_ora = PlanTree(operation="TABLE ACCESS", options={"type": "FULL"})
    validator_ora = MockValidator(plan_ora)

    # Criteria that accepts either
    criteria = ValidationCriteria(expected_constructs=[
        [{"operation": "TABLE ACCESS", "type": "FULL"}, "Seq Scan"]
    ])

    result_pg = validator_pg.validate("SELECT * FROM users", criteria)
    assert result_pg.success is True

    result_ora = validator_ora.validate("SELECT * FROM users", criteria)
    assert result_ora.success is True

    # Negative case: something else
    plan_other = PlanTree(operation="INDEX SCAN")
    validator_other = MockValidator(plan_other)
    result_other = validator_other.validate("SELECT * FROM users", criteria)
    assert result_other.success is False
