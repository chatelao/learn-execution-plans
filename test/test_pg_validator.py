import pytest
from tutorial.validator import PostgresExerciseValidator
from tutorial.models import QueryResult, ValidationCriteria
from tutorial.sandbox import SandboxInterface

class MockSandbox(SandboxInterface):
    def __init__(self, result_to_return: QueryResult):
        self.result_to_return = result_to_return
        self.last_query = None

    def setup_environment(self, db_type: str, init_sql: str) -> None:
        pass

    def execute_query(self, sql: str) -> QueryResult:
        self.last_query = sql
        return self.result_to_return

def test_pg_validator_requests_explain():
    # Simple PG EXPLAIN JSON output
    pg_json = '[{"Plan": {"Node Type": "Seq Scan", "Relation Name": "users"}}]'
    mock_result = QueryResult(columns=["QUERY PLAN"], rows=[(pg_json,)], execution_time=0.1)
    sandbox = MockSandbox(mock_result)
    validator = PostgresExerciseValidator(sandbox)

    criteria = ValidationCriteria(expected_constructs=["Seq Scan"])
    result = validator.validate("SELECT * FROM users", criteria)

    assert "EXPLAIN (FORMAT JSON)" in sandbox.last_query
    assert result.success is True
    assert result.plan_tree.operation == "Seq Scan"

def test_pg_validator_handles_error():
    mock_result = QueryResult(columns=[], rows=[], execution_time=0.0, error="Table not found")
    sandbox = MockSandbox(mock_result)
    validator = PostgresExerciseValidator(sandbox)

    criteria = ValidationCriteria(expected_constructs=["Seq Scan"])
    result = validator.validate("SELECT * FROM non_existent", criteria)

    assert result.success is False
    assert "PostgreSQL EXPLAIN failed: Table not found" in result.feedback

def test_pg_validator_improved_feedback():
    pg_json = '[{"Plan": {"Node Type": "Seq Scan", "Relation Name": "users"}}]'
    mock_result = QueryResult(columns=["QUERY PLAN"], rows=[(pg_json,)], execution_time=0.1)
    sandbox = MockSandbox(mock_result)
    validator = PostgresExerciseValidator(sandbox)

    # Missing complex construct
    criteria = ValidationCriteria(expected_constructs=[
        {"operation": "Index Scan", "Index Name": "idx_u"}
    ])
    result = validator.validate("SELECT * FROM users", criteria)

    assert result.success is False
    assert "Missing expected constructs: (Index Scan Index Name=idx_u)" in result.feedback

def test_pg_validator_forbidden_construct_feedback():
    pg_json = '[{"Plan": {"Node Type": "Seq Scan", "Relation Name": "users"}}]'
    mock_result = QueryResult(columns=["QUERY PLAN"], rows=[(pg_json,)], execution_time=0.1)
    sandbox = MockSandbox(mock_result)
    validator = PostgresExerciseValidator(sandbox)

    # Forbidden simple construct
    criteria = ValidationCriteria(
        expected_constructs=["Seq Scan"],
        forbidden_constructs=["Seq Scan"]
    )
    result = validator.validate("SELECT * FROM users", criteria)

    assert result.success is False
    assert "Forbidden construct found: Seq Scan" in result.feedback
