import pytest
from unittest.mock import MagicMock, patch
from tutorial.sandbox import DockerPostgresSandbox
from tutorial.models import QueryResult
import docker
import psycopg2

@patch("docker.from_env")
def test_sandbox_setup_environment(mock_docker_from_env):
    mock_client = MagicMock()
    mock_docker_from_env.return_value = mock_client

    # Mock container behavior
    mock_container = MagicMock()
    mock_client.containers.run.return_value = mock_container
    mock_client.containers.get.side_effect = docker.errors.NotFound("not found")

    sandbox = DockerPostgresSandbox()

    # Mock psycopg2.connect to succeed immediately
    with patch("psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        sandbox.setup_environment("postgres", "CREATE TABLE test (id int);")

        mock_client.containers.run.assert_called_once()
        mock_connect.assert_called()
        # The cursor is used in a context manager
        mock_conn.cursor.return_value.__enter__.return_value.execute.assert_called_with("CREATE TABLE test (id int);")

@patch("docker.from_env")
def test_sandbox_execute_query(mock_docker_from_env):
    mock_client = MagicMock()
    mock_docker_from_env.return_value = mock_client

    sandbox = DockerPostgresSandbox()

    with patch("psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value.__enter__.return_value
        mock_connect.return_value = mock_conn

        mock_cur.description = [("id",)]
        mock_cur.fetchall.return_value = [(1,)]

        result = sandbox.execute_query("SELECT 1")

        assert result.columns == ["id"]
        assert result.rows == [(1,)]
        assert result.error is None
        mock_cur.execute.assert_called_with("SELECT 1")

@patch("docker.from_env")
def test_sandbox_execute_query_error(mock_docker_from_env):
    mock_client = MagicMock()
    mock_docker_from_env.return_value = mock_client

    sandbox = DockerPostgresSandbox()

    with patch("psycopg2.connect") as mock_connect:
        mock_connect.side_effect = Exception("Connection failed")

        result = sandbox.execute_query("SELECT 1")

        assert result.error == "Connection failed"
        assert result.rows == []

from tutorial.sandbox import DockerOracleSandbox
import oracledb

@patch("docker.from_env")
def test_oracle_sandbox_setup_environment(mock_docker_from_env):
    mock_client = MagicMock()
    mock_docker_from_env.return_value = mock_client

    mock_container = MagicMock()
    mock_client.containers.run.return_value = mock_container
    mock_client.containers.get.side_effect = docker.errors.NotFound("not found")

    sandbox = DockerOracleSandbox()

    with patch("oracledb.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cur = mock_conn.cursor.return_value.__enter__.return_value

        sandbox.setup_environment("oracle", "CREATE TABLE test (id int);")

        mock_client.containers.run.assert_called_once()
        mock_connect.assert_called()
        mock_cur.execute.assert_called_with("CREATE TABLE test (id int);")

@patch("docker.from_env")
def test_oracle_sandbox_execute_query(mock_docker_from_env):
    mock_client = MagicMock()
    mock_docker_from_env.return_value = mock_client

    sandbox = DockerOracleSandbox()

    with patch("oracledb.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cur = mock_conn.cursor.return_value.__enter__.return_value

        mock_cur.description = [("id",)]
        mock_cur.fetchall.return_value = [(1,)]

        result = sandbox.execute_query("SELECT 1")

        assert result.columns == ["id"]
        assert result.rows == [(1,)]
        assert result.error is None
        mock_cur.execute.assert_called_with("SELECT 1")
