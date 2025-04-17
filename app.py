from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# DB 경로 설정
basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(basedir, "tasks.db")

# DB 초기화
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            writer TEXT,
            date TEXT,
            status TEXT
        )
        """)
        conn.commit()

# 메인 페이지
@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
    return render_template('index.html', tasks=tasks)

# 일정 등록
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        writer = request.form.get('writer')
        date_val = request.form.get('date')
        status = request.form.get('status')
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO tasks (title, content, writer, date, status) VALUES (?, ?, ?, ?, ?)",
                      (title, content, writer, date_val, status))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# 일정 수정
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            writer = request.form['writer']
            date_val = request.form['date']
            status = request.form['status']
            c.execute("UPDATE tasks SET title=?, content=?, writer=?, date=?, status=? WHERE id=?",
                      (title, content, writer, date_val, status, task_id))
            conn.commit()
            return redirect(url_for('index'))
        else:
            c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
            task = c.fetchone()
    return render_template('edit.html', task=task)

# 상세 보기
@app.route('/detail/<int:task_id>')
def detail(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task = c.fetchone()
    return render_template('detail.html', task=task)

# 삭제
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
    return redirect(url_for('index'))

# 실행 시 DB 초기화
init_db()
