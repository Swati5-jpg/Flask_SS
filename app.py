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

# Route: View details of a specific student
@app.route('/students/<int:id>', methods=['GET'])
def view_student_detail(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if not student:
        return "Student not found!", 404
    return render_template('student_detail.html', student=student)

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

# Route: Edit student form
@app.route('/students/<int:id>/edit', methods=['GET'])
def edit_student_form(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if not student:
        return "Student not found!", 404
    return render_template('edit_student.html', student=student)

# Route: Update student in the database
@app.route('/students/<int:id>/edit', methods=['POST'])
def edit_student(id):
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    subjects = request.form['subjects']
    
    conn = get_db_connection()
    conn.execute('UPDATE students SET name = ?, age = ?, grade = ?, subjects = ? WHERE id = ?',
                 (name, age, grade, subjects, id))
    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))

# Route: Delete student form (confirmation page)
@app.route('/students/<int:id>/delete', methods=['GET'])
def delete_student_form(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if not student:
        return "Student not found!", 404
    return render_template('delete_student.html', student=student)

# Route: Delete student from the database
@app.route('/students/<int:id>/delete', methods=['POST'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))

# Main application runner
if __name__ == '__main__':
    app.run(debug=True)
