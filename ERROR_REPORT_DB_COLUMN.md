# Flask SQLite error report (DB column mismatch)

## Symptom
Submitting the form to `POST /add` raised:

- `sqlite3.OperationalError: table users has no column named Designation`

## What was happening
After fixing the DB path, the app started using the DB file at `Ecom/users.db`, but that existing database already had a different schema:

```sql
PRAGMA table_info(users);
```
returned only:
- `id`
- `name`

So the table `users` did **not** contain the `Designation` column, while the app was trying to insert into:

```sql
INSERT INTO users (name, Designation) ...
```

## Root cause
`init_db()` used `CREATE TABLE IF NOT EXISTS users (...)`.

Because the table already existed (from a previous run), SQLite did **not** apply the newer schema that includes the `Designation` column.

## Solution implemented
Update the DB initialization so it can migrate/repair the existing schema:

1. On startup, ensure the DB table exists.
2. Check if the `Designation` column exists.
3. If missing, run an `ALTER TABLE` to add the column.

This makes the app resilient when `users.db` already exists.

## Files changed
- `app.py`: added schema migration logic (ALTER TABLE for missing `Designation` column).

## How to verify
1. Restart the Flask app.
2. Submit the form.
3. Confirm `POST /add` returns success and the row is displayed in `/`.

