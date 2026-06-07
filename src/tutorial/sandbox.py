import time
import docker
import psycopg2
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from .models import QueryResult

class SandboxInterface(ABC):
    """
    Database Sandbox Interface (DSI)
    A wrapper around Docker to manage database lifecycles.
    """

    @abstractmethod
    def setup_environment(self, db_type: str, init_sql: str) -> None:
        """
        Prepares the container with the required schema.

        :param db_type: 'oracle' or 'postgres'
        :param init_sql: SQL script to initialize the database schema.
        """
        pass

    @abstractmethod
    def execute_query(self, sql: str) -> QueryResult:
        """
        Executes a query and returns results.

        :param sql: SQL statement to execute.
        :return: A QueryResult object containing columns, rows, and execution time.
        """
        pass

class PostgresSandbox(SandboxInterface):
    """
    Concrete implementation of SandboxInterface for PostgreSQL using Docker.
    """

    def __init__(self, image: str = "postgres:latest", container_name: str = "tutorial-postgres", port: int = 5432):
        try:
            self.client = docker.from_env()
        except Exception:
            # Fallback for environments where docker-py might be installed but docker daemon is not accessible
            self.client = None

        self.image = image
        self.container_name = container_name
        self.container: Optional[Any] = None
        self.db_params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "password",
            "host": "localhost",
            "port": port
        }

    def setup_environment(self, db_type: str, init_sql: str) -> None:
        if db_type.lower() != "postgres":
            raise ValueError(f"PostgresSandbox does not support {db_type}")

        if self.client is None:
             raise RuntimeError("Docker client not initialized. Ensure Docker is running.")

        # Ensure container is running
        self._ensure_container_running()

        # Wait for PostgreSQL to be ready
        self._wait_for_postgres()

        # Execute init_sql
        if init_sql:
            res = self.execute_query(init_sql)
            if res.error:
                raise RuntimeError(f"Failed to initialize database: {res.error}")

    def execute_query(self, sql: str) -> QueryResult:
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor()

            start_time = time.time()
            cur.execute(sql)

            columns = []
            rows = []
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()

            conn.commit()
            execution_time = time.time() - start_time

            return QueryResult(columns=columns, rows=rows, execution_time=execution_time)
        except Exception as e:
            if conn:
                conn.rollback()
            return QueryResult(columns=[], rows=[], execution_time=0.0, error=str(e))
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def _ensure_container_running(self):
        try:
            self.container = self.client.containers.get(self.container_name)
            if self.container.status != "running":
                self.container.start()
        except docker.errors.NotFound:
            self.container = self.client.containers.run(
                self.image,
                name=self.container_name,
                environment={"POSTGRES_PASSWORD": self.db_params["password"]},
                ports={f"5432/tcp": self.db_params["port"]},
                detach=True
            )

    def _wait_for_postgres(self, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                conn = psycopg2.connect(**self.db_params)
                conn.close()
                return
            except psycopg2.OperationalError:
                time.sleep(1)
        raise TimeoutError("PostgreSQL container did not become ready in time.")
