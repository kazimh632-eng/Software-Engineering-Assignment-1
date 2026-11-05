from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = Path(__file__).with_name('students.db')

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )''')

@app.get('/students')
def get_students():
    with connect() as db:
        rows = db.execute('SELECT * FROM students ORDER BY id').fetchall()
    return jsonify([dict(row) for row in rows])

@app.get('/students/<int:student_id>')
def get_student(student_id):
    with connect() as db:
        row = db.execute('SELECT * FROM students WHERE id=?', (student_id,)).fetchone()
    if row is None:
        return jsonify(error='Student not found'), 404
    return jsonify(dict(row))

def student_payload():
    data = request.get_json(silent=True) or {}
    fields = {key: str(data.get(key, '')).strip() for key in ('name', 'department', 'email')}
    missing = [key for key, value in fields.items() if not value]
    if missing:
        return None, (jsonify(error='Required fields: name, department, email'), 400)
    return fields, None

@app.post('/students')
def add_student():
    data, error = student_payload()
    if error: return error
    try:
        with connect() as db:
            cur = db.execute('INSERT INTO students(name, department, email) VALUES (?, ?, ?)',
                             (data['name'], data['department'], data['email']))
            row = db.execute('SELECT * FROM students WHERE id=?', (cur.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify(error='Email already exists'), 409

@app.put('/students/<int:student_id>')
def update_student(student_id):
    data, error = student_payload()
    if error: return error
    try:
        with connect() as db:
            cur = db.execute('UPDATE students SET name=?, department=?, email=? WHERE id=?',
                             (data['name'], data['department'], data['email'], student_id))
            if cur.rowcount == 0: return jsonify(error='Student not found'), 404
            row = db.execute('SELECT * FROM students WHERE id=?', (student_id,)).fetchone()
        return jsonify(dict(row))
    except sqlite3.IntegrityError:
        return jsonify(error='Email already exists'), 409

@app.delete('/students/<int:student_id>')
def delete_student(student_id):
    with connect() as db:
        cur = db.execute('DELETE FROM students WHERE id=?', (student_id,))
    if cur.rowcount == 0: return jsonify(error='Student not found'), 404
    return jsonify(message='Student deleted')

init_db()
if __name__ == '__main__':
    app.run(debug=True, port=5001)
