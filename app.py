from typing import Any

from mcp.server.mcpserver import MCPServer

from todo_service import TodoService


mcp = MCPServer("Appwrite Todo")
_service: TodoService | None = None


def service() -> TodoService:
    global _service
    if _service is None:
        _service = TodoService()
    return _service


@mcp.tool()
def add_task(
    title: str,
    description: str | None = None,
    due_date: str | None = None,
    priority: int = 2,
    category: str | None = None,
    tags: str | None = None,
) -> dict[str, Any]:
    """Create a Todo task in Appwrite.

    priority: 1 = high, 2 = medium, 3 = low.
    due_date should be an ISO-8601 datetime when supplied.
    """
    return service().add_task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        category=category,
        tags=tags,
    )


@mcp.tool()
def list_tasks(
    completed: bool | None = None,
    category: str | None = None,
    limit: int = 25,
) -> dict[str, Any]:
    """List Todo tasks, optionally filtered by completion state or category."""
    return service().list_tasks(
        completed=completed,
        category=category,
        limit=limit,
    )


@mcp.tool()
def get_task(task_id: str) -> dict[str, Any]:
    """Get one Todo task by its Appwrite row ID."""
    return service().get_task(task_id)


@mcp.tool()
def update_task(
    task_id: str,
    title: str | None = None,
    description: str | None = None,
    due_date: str | None = None,
    priority: int | None = None,
    completed: bool | None = None,
    category: str | None = None,
    tags: str | None = None,
) -> dict[str, Any]:
    """Update one or more fields of an existing Todo task."""
    return service().update_task(
        task_id=task_id,
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        completed=completed,
        category=category,
        tags=tags,
    )


@mcp.tool()
def complete_task(task_id: str) -> dict[str, Any]:
    """Mark a Todo task as completed."""
    return service().complete_task(task_id)


@mcp.tool()
def delete_task(task_id: str) -> dict[str, Any]:
    """Permanently delete a Todo task."""
    return service().delete_task(task_id)


if __name__ == "__main__":
    # Streamable HTTP is the transport we will use when the server is deployed.
    # The stateless JSON mode is also convenient for a small personal server.
    mcp.run(
        transport="streamable-http",
        stateless_http=True,
        json_response=True,
    )
