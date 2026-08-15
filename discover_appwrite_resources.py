"""Discover Appwrite TablesDB databases and tables using values from .env.

Usage:
    python discover_appwrite_resources.py

It reads `APPWRITE_ENDPOINT`, `APPWRITE_PROJECT_ID`, and `APPWRITE_API_KEY` from .env
and calls the Appwrite TablesDB admin endpoints to list databases and tables.
"""
import os
import sys
import json
from typing import Any
import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
API_KEY = os.getenv("APPWRITE_API_KEY")

if not (ENDPOINT and PROJECT_ID and API_KEY):
    print("Missing APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID or APPWRITE_API_KEY in .env", file=sys.stderr)
    sys.exit(2)

# Ensure endpoint doesn't end with a slash
ENDPOINT = ENDPOINT.rstrip('/')

HEADERS = {
    "X-Appwrite-Project": PROJECT_ID,
    "X-Appwrite-Key": API_KEY,
    "Content-Type": "application/json",
}


def api_get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    url = ENDPOINT + path
    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        print(f"Request to {url} failed: {r.status_code}", file=sys.stderr)
        try:
            print(r.json(), file=sys.stderr)
        except Exception:
            print(r.text, file=sys.stderr)
        sys.exit(1)
    return r.json()


def list_databases() -> list[dict[str, Any]]:
    # Appwrite TablesDB list databases endpoint
    return api_get("/tablesdb").get("databases", [])


def list_tables(database_id: str) -> list[dict[str, Any]]:
    return api_get(f"/tablesdb/{database_id}/tables").get("tables", [])


def main() -> None:
    print("Discovering Appwrite TablesDB databases...")
    dbs = list_databases()
    if not dbs:
        print("No TablesDB databases found.")
        return
    print(json.dumps(dbs, indent=2))
    print("\nTables per database:")
    for db in dbs:
        db_id = db.get("$id") or db.get("id") or db.get("$uid") or db.get("$databaseId") or db.get("id")
        name = db.get("name") or db.get("$name") or db_id
        print(f"\nDatabase: {name} (id: {db_id})")
        tables = list_tables(db_id)
        if not tables:
            print("  (no tables)")
            continue
        for t in tables:
            t_id = t.get("$id") or t.get("id") or t.get("name")
            t_name = t.get("name") or t_id
            print(f"  - {t_name} (id: {t_id})")


if __name__ == "__main__":
    main()
