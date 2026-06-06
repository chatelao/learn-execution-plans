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
