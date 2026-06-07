from abc import ABC, abstractmethod
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

import docker
import psycopg2
import oracledb
import time

class DockerPostgresSandbox(SandboxInterface):
    """
    A sandbox implementation that uses a Docker container for PostgreSQL.
    """

    def __init__(self, image: str = "postgres:alpine", container_name: str = "pg-sandbox"):
        self.image = image
        self.container_name = container_name
        self.client = docker.from_env()
        self.container = None
        self.db_params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "password",
            "host": "localhost",
            "port": 5432
        }

    def setup_environment(self, db_type: str, init_sql: str) -> None:
        if db_type.lower() != "postgres":
            raise ValueError(f"Unsupported db_type: {db_type}")

        # Stop and remove existing container if it exists
        try:
            existing = self.client.containers.get(self.container_name)
            existing.stop()
            existing.remove()
        except docker.errors.NotFound:
            pass

        # Start new container
        self.container = self.client.containers.run(
            self.image,
            name=self.container_name,
            environment={"POSTGRES_PASSWORD": self.db_params["password"]},
            ports={f"{self.db_params['port']}/tcp": self.db_params["port"]},
            detach=True
        )

        # Wait for PostgreSQL to be ready
        retries = 30
        conn = None
        while retries > 0:
            try:
                conn = psycopg2.connect(**self.db_params)
                break
            except psycopg2.OperationalError:
                retries -= 1
                time.sleep(1)

        if not conn:
            raise RuntimeError("Failed to connect to PostgreSQL in Docker container")

        # Run initialization SQL
        try:
            with conn.cursor() as cur:
                cur.execute(init_sql)
            conn.commit()
        finally:
            conn.close()

    def execute_query(self, sql: str) -> QueryResult:
        start_time = time.perf_counter()
        conn = None
        try:
            conn = psycopg2.connect(**self.db_params)
            with conn.cursor() as cur:
                cur.execute(sql)
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                else:
                    columns = []
                    rows = []
                conn.commit()
                execution_time = time.perf_counter() - start_time
                return QueryResult(columns=columns, rows=rows, execution_time=execution_time)
        except Exception as e:
            return QueryResult(columns=[], rows=[], execution_time=0, error=str(e))
        finally:
            if conn:
                conn.close()

    def stop(self):
        """Stops and removes the sandbox container."""
        if self.container:
            self.container.stop()
            self.container.remove()
            self.container = None

class DockerOracleSandbox(SandboxInterface):
    """
    A sandbox implementation that uses a Docker container for Oracle Database.
    """

    def __init__(self, image: str = "gvenzl/oracle-free", container_name: str = "oracle-sandbox"):
        self.image = image
        self.container_name = container_name
        self.client = docker.from_env()
        self.container = None
        self.db_params = {
            "user": "system",
            "password": "password",
            "dsn": "localhost:1521/FREEPDB1"
        }

    def setup_environment(self, db_type: str, init_sql: str) -> None:
        if db_type.lower() != "oracle":
            raise ValueError(f"Unsupported db_type: {db_type}")

        # Stop and remove existing container if it exists
        try:
            existing = self.client.containers.get(self.container_name)
            existing.stop()
            existing.remove()
        except docker.errors.NotFound:
            pass

        # Start new container
        self.container = self.client.containers.run(
            self.image,
            name=self.container_name,
            environment={"ORACLE_PASSWORD": self.db_params["password"]},
            ports={"1521/tcp": 1521},
            detach=True
        )

        # Wait for Oracle to be ready
        retries = 60
        conn = None
        while retries > 0:
            try:
                conn = oracledb.connect(
                    user=self.db_params["user"],
                    password=self.db_params["password"],
                    dsn=self.db_params["dsn"]
                )
                break
            except Exception:
                retries -= 1
                time.sleep(5)

        if not conn:
            raise RuntimeError("Failed to connect to Oracle in Docker container")

        # Run initialization SQL
        try:
            with conn.cursor() as cur:
                cur.execute(init_sql)
            conn.commit()
        finally:
            conn.close()

    def execute_query(self, sql: str) -> QueryResult:
        start_time = time.perf_counter()
        conn = None
        try:
            conn = oracledb.connect(
                user=self.db_params["user"],
                password=self.db_params["password"],
                dsn=self.db_params["dsn"]
            )
            with conn.cursor() as cur:
                cur.execute(sql)
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                else:
                    columns = []
                    rows = []
                conn.commit()
                execution_time = time.perf_counter() - start_time
                return QueryResult(columns=columns, rows=rows, execution_time=execution_time)
        except Exception as e:
            return QueryResult(columns=[], rows=[], execution_time=0, error=str(e))
        finally:
            if conn:
                conn.close()

    def stop(self):
        """Stops and removes the sandbox container."""
        if self.container:
            self.container.stop()
            self.container.remove()
            self.container = None
