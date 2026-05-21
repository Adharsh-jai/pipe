from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()


# Home page
@app.route('/')
def home():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template('index.html', users=users)


# Add user
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)