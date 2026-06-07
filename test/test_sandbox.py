import pytest
from unittest.mock import MagicMock, patch
from tutorial.sandbox import DockerSandbox

@patch("docker.from_env")
def test_sandbox_teardown(mock_docker):
    mock_container = MagicMock()
    sandbox = DockerSandbox()
    sandbox.container = mock_container

    sandbox.teardown()

    mock_container.stop.assert_called_once()
    assert sandbox.container is None

@patch("docker.from_env")
@patch("psycopg2.connect")
def test_sandbox_setup_postgres(mock_connect, mock_docker):
    mock_client = mock_docker.return_value
    mock_container = MagicMock()
    mock_client.containers.run.return_value = mock_container

    mock_conn = mock_connect.return_value
    mock_cur = mock_conn.cursor.return_value.__enter__.return_value

    sandbox = DockerSandbox()
    sandbox.setup_environment("postgres", "CREATE TABLE test();")

    mock_client.containers.run.assert_called_once()
    mock_cur.execute.assert_called_with("CREATE TABLE test();")
    mock_conn.commit.assert_called_once()

@patch("docker.from_env")
@patch("psycopg2.connect")
def test_sandbox_execute_query_postgres(mock_connect, mock_docker):
    mock_conn = mock_connect.return_value
    mock_cur = mock_conn.cursor.return_value.__enter__.return_value
    mock_cur.fetchall.return_value = [("val1",), ("val2",)]
    mock_cur.description = [("col1",)]

    sandbox = DockerSandbox()
    sandbox.container = MagicMock()
    sandbox.db_type = "postgres"

    result = sandbox.execute_query("SELECT * FROM test;")

    assert result.columns == ["col1"]
    assert result.rows == [("val1",), ("val2",)]
    assert result.error is None
    mock_cur.execute.assert_called_with("SELECT * FROM test;")
