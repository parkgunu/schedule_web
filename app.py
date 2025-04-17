from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def init_db():
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        content TEXT,
                        writer TEXT,
                        date TEXT,
                        status TEXT)''')

@app.route('/')
def index():
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        writer = request.form['writer']
        date_val = request.form['date']
        status = request.form['status']
        with sqlite3.connect("tasks.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO tasks (title, content, writer, date, status) VALUES (?, ?, ?, ?, ?)",
                      (title, content, writer, date_val, status))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            writer = request.form['writer']
            date_val = request.form['date']
            status = request.form['status']
            c.execute("UPDATE tasks SET title=?, content=?, writer=?, date=?, status=? WHERE id=?",
                      (title, content, writer, date_val, status, task_id))
            return redirect(url_for('index'))
        else:
            c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
            task = c.fetchone()
    return render_template('edit.html', task=task)

@app.route('/detail/<int:task_id>')
def detail(task_id):
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task = c.fetchone()
    return render_template('detail.html', task=task)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
import sqlite3

def init_db():
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
        """)
        conn.commit()

# 앱 실행 전에 DB 초기화
init_db()
