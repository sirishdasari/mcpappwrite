"""Simple Appwrite connectivity test.

Run after filling in .env:
    python test_appwrite.py
"""

from todo_service import TodoService


if __name__ == "__main__":
    todo = TodoService()
    result = todo.list_tasks(limit=5)
    print("Appwrite connection successful.")
    print(f"Rows returned: {len(result.get('rows', []))}")
    for row in result.get("rows", []):
        print(row)
