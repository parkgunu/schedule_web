from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# 1. Flask 앱 생성
app = Flask(__name__)

# 2. 환경변수 로드
load_dotenv()

# 3. PostgreSQL 연결 설정
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. SQLAlchemy 초기화
db = SQLAlchemy(app)

# 5. Task 모델 정의
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    writer = db.Column(db.String(50))
    date = db.Column(db.String(20))
    status = db.Column(db.String(20))

# 6. DB 생성
with app.app_context():
    db.create_all()

# 메인 페이지
@app.route('/')
def index():
    filter_status = request.args.get('status')
    if filter_status and filter_status != '전체':
        tasks = Task.query.filter_by(status=filter_status).order_by(Task.date).all()
    else:
        tasks = Task.query.order_by(Task.date).all()
    return render_template('index.html', tasks=tasks, current_filter=filter_status or '전체')

# 일정 등록
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        task = Task(
            title=request.form['title'],
            content=request.form['content'],
            writer=request.form['writer'],
            date=request.form['date'],
            status=request.form['status']
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# 일정 수정
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.content = request.form['content']
        task.writer = request.form['writer']
        task.date = request.form['date']
        task.status = request.form['status']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

# 상세 보기
@app.route('/detail/<int:task_id>')
def detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('detail.html', task=task)

# 삭제
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
