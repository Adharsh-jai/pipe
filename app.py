from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Create database and table
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')

# Create database and table
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table with the expected schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            Designation TEXT NOT NULL
        )
    ''')

    # Handle existing DBs created with an older schema (missing `Designation`)
    cursor.execute("PRAGMA table_info(users)")
    columns = {row[1] for row in cursor.fetchall()}  # row[1] == column name

    if 'Designation' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN Designation TEXT")

    conn.commit()
    conn.close()

init_db()


# Home page
@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template('index.html', users=users)


# Add user
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    Designation = request.form['Designation']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, Designation) VALUES (?, ?)", (name, Designation))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)