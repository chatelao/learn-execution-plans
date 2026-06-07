import pytest
from unittest.mock import MagicMock, patch
from tutorial.sandbox import PostgresSandbox
from tutorial.models import QueryResult
import docker
import psycopg2

@patch("docker.from_env")
def test_postgres_sandbox_init(mock_docker_from_env):
    mock_client = MagicMock()
    mock_docker_from_env.return_value = mock_client

    sandbox = PostgresSandbox(container_name="test-container")

    assert sandbox.container_name == "test-container"
    assert sandbox.client == mock_client

@patch("psycopg2.connect")
def test_postgres_sandbox_execute_query(mock_connect):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur

    # Mock some query results
    mock_cur.description = [("col1",), ("col2",)]
    mock_cur.fetchall.return_value = [("val1", "val2")]

    sandbox = PostgresSandbox()
    result = sandbox.execute_query("SELECT * FROM test")

    assert result.columns == ["col1", "col2"]
    assert result.rows == [("val1", "val2")]
    assert result.error is None
    mock_cur.execute.assert_called_with("SELECT * FROM test")
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("psycopg2.connect")
def test_postgres_sandbox_execute_query_error(mock_connect):
    mock_connect.side_effect = Exception("Connection failed")

    sandbox = PostgresSandbox()
    result = sandbox.execute_query("SELECT 1")

    assert result.error == "Connection failed"
    assert result.columns == []
    assert result.rows == []

@patch("docker.from_env")
def test_postgres_sandbox_setup_environment(mock_docker_from_env):
    mock_client = MagicMock()
    mock_docker_from_env.return_value = mock_client

    # Mock container
    mock_container = MagicMock()
    mock_container.status = "running"
    mock_client.containers.get.return_value = mock_container

    sandbox = PostgresSandbox()

    # Mock _wait_for_postgres and execute_query
    with patch.object(sandbox, "_wait_for_postgres") as mock_wait:
        with patch.object(sandbox, "execute_query") as mock_exec:
            mock_exec.return_value = QueryResult(columns=[], rows=[], execution_time=0.1)

            sandbox.setup_environment("postgres", "CREATE TABLE x")

            mock_client.containers.get.assert_called_with(sandbox.container_name)
            mock_wait.assert_called_once()
            mock_exec.assert_called_with("CREATE TABLE x")

def test_postgres_sandbox_setup_environment_wrong_db():
    sandbox = PostgresSandbox()
    with pytest.raises(ValueError, match="does not support oracle"):
        sandbox.setup_environment("oracle", "...")
