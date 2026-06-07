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

    @abstractmethod
    def teardown(self) -> None:
        """
        Cleans up resources (e.g., stops and removes containers).
        """
        pass

class DockerSandbox(SandboxInterface):
    """
    Concrete implementation of SandboxInterface using Docker SDK.
    Currently supports PostgreSQL.
    """

    def __init__(self, image_pg: str = "postgres:latest", config: Optional[Dict[str, Any]] = None):
        self.client = docker.from_env()
        self.image_pg = image_pg
        self.container: Optional[docker.models.containers.Container] = None
        self.db_type: Optional[str] = None

        # Configuration with defaults
        self.config = config or {}
        self.port = self.config.get("port", 54321)
        self.user = self.config.get("user", "postgres")
        self.password = self.config.get("password", "password")
        self.dbname = self.config.get("dbname", "tutorial")

    def setup_environment(self, db_type: str, init_sql: str) -> None:
        self.db_type = db_type.lower()
        if self.db_type == "postgres":
            self._setup_postgres(init_sql)
        else:
            raise NotImplementedError(f"Database type '{db_type}' not supported yet.")

    def _setup_postgres(self, init_sql: str) -> None:
        if self.container:
            self.teardown()

        self.container = self.client.containers.run(
            self.image_pg,
            detach=True,
            environment={
                "POSTGRES_PASSWORD": self.password,
                "POSTGRES_DB": self.dbname
            },
            ports={'5432/tcp': self.port},
            auto_remove=True
        )

        # Wait for Postgres to be ready
        retries = 30
        conn = None
        while retries > 0:
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    dbname=self.dbname
                )
                break
            except psycopg2.OperationalError:
                retries -= 1
                time.sleep(1)

        if not conn:
            raise RuntimeError("Failed to connect to PostgreSQL container.")

        try:
            with conn.cursor() as cur:
                cur.execute(init_sql)
            conn.commit()
        finally:
            conn.close()

    def execute_query(self, sql: str) -> QueryResult:
        if not self.container:
            raise RuntimeError("Sandbox environment not set up.")

        start_time = time.perf_counter()
        conn = None
        try:
            if self.db_type == "postgres":
                conn = psycopg2.connect(
                    host="localhost",
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    dbname=self.dbname
                )
            else:
                raise RuntimeError(f"Unsupported db_type: {self.db_type}")

            with conn.cursor() as cur:
                cur.execute(sql)
                try:
                    rows = cur.fetchall()
                    columns = [desc[0] for desc in cur.description]
                except psycopg2.ProgrammingError:
                    # For statements that don't return rows (like EXPLAIN sometimes if not handled correctly)
                    rows = []
                    columns = []

            execution_time = time.perf_counter() - start_time
            return QueryResult(columns=columns, rows=rows, execution_time=execution_time)
        except Exception as e:
            return QueryResult(columns=[], rows=[], execution_time=0, error=str(e))
        finally:
            if conn:
                conn.close()

    def teardown(self) -> None:
        if self.container:
            try:
                self.container.stop()
            except Exception:
                pass
            self.container = None
