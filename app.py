from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route: Root URL redirects to the students list
@app.route('/')
def home():
    return redirect(url_for('view_students'))

# Route: View all students
@app.route('/students', methods=['GET'])
def view_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('students.html', students=students)

# Route: Add a new student form
@app.route('/add-student-form', methods=['GET'])
def add_student_form():
    return render_template('add_student.html')  # Template for adding a new student

# Route: Add a new student to the database
@app.route('/students', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    subjects = request.form['subjects']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO students (name, age, grade, subjects) VALUES (?, ?, ?, ?)',
                 (name, age, grade, subjects))
    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))

# Main application runner
if __name__ == '__main__':
    app.run(debug=True)
