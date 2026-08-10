import os
from typing import Any

from appwrite.client import Client
from appwrite.id import ID
from appwrite.services.tables_db import TablesDB
from appwrite.query import Query
from dotenv import load_dotenv

load_dotenv()


class TodoService:
    """Small Appwrite TablesDB wrapper for the Todo MCP server."""

    def __init__(self) -> None:
        endpoint = os.getenv("APPWRITE_ENDPOINT")
        project_id = os.getenv("APPWRITE_PROJECT_ID")
        api_key = os.getenv("APPWRITE_API_KEY")
        self.database_id = os.getenv("APPWRITE_DATABASE_ID", "todo_db")
        self.table_id = os.getenv("APPWRITE_TABLE_ID", "tasks")

        missing = [
            name
            for name, value in {
                "APPWRITE_ENDPOINT": endpoint,
                "APPWRITE_PROJECT_ID": project_id,
                "APPWRITE_API_KEY": api_key,
            }.items()
            if not value
        ]
        if missing:
            raise RuntimeError(
                "Missing required environment variables: " + ", ".join(missing)
            )

        client = Client()
        client.set_endpoint(endpoint)
        client.set_project(project_id)
        client.set_key(api_key)
        self.tables_db = TablesDB(client)

    @staticmethod
    def _row_to_dict(row: Any) -> dict[str, Any]:
        """Convert an Appwrite Row/model to a plain JSON-compatible dictionary."""
        if hasattr(row, "model_dump"):
            return row.model_dump()
        if isinstance(row, dict):
            return row
        return {
            "id": getattr(row, "$id", getattr(row, "id", None)),
            "data": getattr(row, "data", {}),
        }

    def add_task(
        self,
        title: str,
        description: str | None = None,
        due_date: str | None = None,
        priority: int = 2,
        completed: bool = False,
        category: str | None = None,
        tags: str | None = None,
    ) -> dict[str, Any]:
        if priority not in (1, 2, 3):
            raise ValueError("priority must be 1 (high), 2 (medium), or 3 (low)")

        data: dict[str, Any] = {
            "title": title,
            "priority": priority,
            "completed": completed,
        }
        optional = {
            "description": description,
            "dueDate": due_date,
            "category": category,
            "tags": tags,
        }
        data.update({key: value for key, value in optional.items() if value is not None})

        row = self.tables_db.create_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=ID.unique(),
            data=data,
        )
        return self._row_to_dict(row)

    def list_tasks(
        self,
        completed: bool | None = None,
        category: str | None = None,
        limit: int = 25,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 100))
        queries = [Query.order_asc("dueDate"), Query.limit(limit)]

        if completed is not None:
            queries.insert(0, Query.equal("completed", completed))
        if category:
            queries.insert(0, Query.equal("category", category))

        result = self.tables_db.list_rows(
            database_id=self.database_id,
            table_id=self.table_id,
            queries=queries,
        )

        if hasattr(result, "model_dump"):
            return result.model_dump()
        if isinstance(result, dict):
            return result
        return {"total": len(getattr(result, "rows", [])), "rows": [self._row_to_dict(r) for r in result.rows]}

    def get_task(self, task_id: str) -> dict[str, Any]:
        row = self.tables_db.get_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=task_id,
        )
        return self._row_to_dict(row)

    def update_task(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None,
        due_date: str | None = None,
        priority: int | None = None,
        completed: bool | None = None,
        category: str | None = None,
        tags: str | None = None,
    ) -> dict[str, Any]:
        if priority is not None and priority not in (1, 2, 3):
            raise ValueError("priority must be 1 (high), 2 (medium), or 3 (low)")

        data: dict[str, Any] = {}
        values = {
            "title": title,
            "description": description,
            "dueDate": due_date,
            "priority": priority,
            "completed": completed,
            "category": category,
            "tags": tags,
        }
        data.update({key: value for key, value in values.items() if value is not None})

        if not data:
            return self.get_task(task_id)

        row = self.tables_db.update_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=task_id,
            data=data,
        )
        return self._row_to_dict(row)

    def complete_task(self, task_id: str) -> dict[str, Any]:
        row = self.tables_db.update_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=task_id,
            data={"completed": True},
        )
        return self._row_to_dict(row)

    def delete_task(self, task_id: str) -> dict[str, Any]:
        self.tables_db.delete_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=task_id,
        )
        return {"success": True, "task_id": task_id}
