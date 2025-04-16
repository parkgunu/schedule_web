from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime, date
import os

app = Flask(__name__)
DB_NAME = 'tasks.db'

STATUS_LABELS = {
    "To-Do": "예정",
    "In Progress": "진행중",
    "Done": "완료"
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            assignee TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'To-Do',
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, assignee, due_date, status, created_at FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()
    conn.close()
    return task

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, assignee, due_date, status FROM tasks ORDER BY due_date ASC")
    tasks = c.fetchall()
    today = date.today().isoformat()
    c.execute("SELECT id, title FROM tasks WHERE due_date = ? AND status != 'Done'", (today,))
    alerts = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks, current_status=None, alerts=alerts, status_labels=STATUS_LABELS)

@app.route('/status/<status>')
def filter_by_status(status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, assignee, due_date, status FROM tasks WHERE status = ? ORDER BY due_date ASC", (status,))
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks, current_status=status, alerts=[], status_labels=STATUS_LABELS)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        assignee = request.form['assignee']
        due_date = request.form['due_date']
        status = request.form['status']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title, assignee, due_date, status, created_at) VALUES (?, ?, ?, ?, ?)",
                  (title, assignee, due_date, status, datetime.now()))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html', status_labels=STATUS_LABELS)

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = get_task(task_id)
    return render_template('detail.html', task=task, status_labels=STATUS_LABELS)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if request.method == 'POST':
        title = request.form['title']
        assignee = request.form['assignee']
        due_date = request.form['due_date']
        status = request.form['status']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE tasks SET title = ?, assignee = ?, due_date = ?, status = ? WHERE id = ?",
                  (title, assignee, due_date, status, task_id))
        conn.commit()
        conn.close()
        return redirect('/')
    task = get_task(task_id)
    return render_template('edit.html', task=task, status_labels=STATUS_LABELS)

@app.route('/done/<int:task_id>')
def mark_done(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
