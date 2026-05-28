# Flask SQLite error report

## Symptom (typical runtime error)
When running the Flask app in environments where the **current working directory changes** (Docker/Jenkins/cron/systemd), SQLite may fail with errors like:
- `sqlite3.OperationalError: unable to open database file`
- missing table errors (if DB is created in a different directory)

## Root cause
In `app.py`, the database is opened using a **relative path**:

```py
sqlite3.connect('users.db')
```

Relative paths depend on the process working directory. When Flask is launched from a different directory, the app may read/write `users.db` somewhere else (or fail to create it), breaking the app.

## Solution implemented
Use an **absolute database path** based on the directory of `app.py`:

```py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')

conn = sqlite3.connect(DB_PATH)
```

This ensures the same `users.db` file is always used no matter where `python app.py` is launched from.

## Files changed
- `app.py`: replaced `sqlite3.connect('users.db')` with `sqlite3.connect(DB_PATH)`

## How to verify
1. Start the app from any directory (or via Docker/Jenkins).
2. Submit the form on `/`.
3. Confirm rows appear in the UI and the DB file updates.

