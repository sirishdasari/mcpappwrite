# mcpappwrite

A minimal Python MCP Todo server backed by Appwrite Cloud.

The project is intentionally small: ChatGPT/MCP clients call Todo tools, and the server stores the data in an Appwrite TablesDB table.

## Architecture

```text
MCP client / ChatGPT
        |
        v
   Python MCP server
        |
        v
   Appwrite TablesDB
        |
        v
      tasks
```

## Requirements

- Python 3.10+
- An Appwrite Cloud project
- An Appwrite server API key with row read/write access

## Appwrite setup

Create a database and a table named `tasks` (the IDs can also be custom):

- Database ID: `todo_db`
- Table ID: `tasks`

Create these columns:

| Column | Type | Required | Notes |
|---|---|---:|---|
| `title` | Varchar | Yes | Task title |
| `description` | Text | No | Details |
| `dueDate` | Datetime | No | ISO-8601 datetime |
| `priority` | Integer | No | 1 high, 2 medium, 3 low |
| `completed` | Boolean | No | Default `false` |
| `category` | Varchar | No | Example: Career |
| `tags` | Varchar | No | Comma-separated tags |

For the server API key, grant only the database/table/row scopes required for this project. Do not put the API key in source code.

## Local setup

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS/Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your Appwrite values.

```env
APPWRITE_ENDPOINT=https://<REGION>.cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_server_api_key
APPWRITE_DATABASE_ID=todo_db
APPWRITE_TABLE_ID=tasks
```

## Run

The server uses MCP Streamable HTTP so it can later be deployed as a remote MCP server.

```bash
python app.py
```

The MCP endpoint is normally:

```text
http://localhost:8000/mcp
```

For a quick local tool test, use the MCP Inspector or another MCP client.

## Available tools

- `add_task` - create a task
- `list_tasks` - list tasks, optionally filtering completed status/category
- `get_task` - retrieve one task by row ID
- `update_task` - update selected task fields
- `complete_task` - mark a task complete
- `delete_task` - delete a task

## Security

`.env` is ignored by Git. Never commit an Appwrite API key. For production, put the secret in the hosting platform's secret/environment-variable system.

## Future steps

1. Test Appwrite connection locally.
2. Test every MCP tool locally.
3. Add authentication for a remote deployment.
4. Deploy the MCP server on a free-tier host.
5. Connect the remote MCP server to a compatible MCP client.
