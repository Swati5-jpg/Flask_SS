import unittest
from app import app, get_db_connection
import sqlite3

class TestStudentManagement(unittest.TestCase):

    def setUp(self):
        """ Set up a fresh database and the test client before each test """
        self.app = app.test_client()
        self.app.testing = True

        # Create a fresh database for testing
        with app.app_context():
            conn = get_db_connection()
            conn.execute('DROP TABLE IF EXISTS students')
            conn.execute(''' 
                CREATE TABLE students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade TEXT NOT NULL,
                    subjects TEXT NOT NULL
                )
            ''')
            conn.commit()
            conn.close()

    def test_add_student(self):
        """ Test adding a new student """
        response = self.app.post('/students', data={
            'name': 'Amit Sharma',
            'age': '20',
            'grade': 'A',
            'subjects': 'Mathematics, Physics'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after adding

        # Verify the student is added to the database
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE name = "Amit Sharma"')
        student = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(student)
        self.assertEqual(student[1], 'Amit Sharma')
        self.assertEqual(student[2], 20)
        self.assertEqual(student[3], 'A')
        self.assertEqual(student[4], 'Mathematics, Physics')

    def test_view_students(self):
        """ Test viewing all students """
        # Add a student for testing
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, age, grade, subjects) VALUES (?, ?, ?, ?)',
                       ('Priya Deshmukh', 22, 'B', 'English, History'))
        conn.commit()
        conn.close()

        # Make GET request to view students
        response = self.app.get('/students')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Priya Deshmukh', response.data)

    def test_view_student_detail(self):
        """ Test viewing details of a specific student """
        # Add a student for testing
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, age, grade, subjects) VALUES (?, ?, ?, ?)',
                       ('Ravi Kumar', 21, 'B', 'Computer Science, Engineering'))
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()

        # Make GET request to view student details
        response = self.app.get(f'/students/{student_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ravi Kumar', response.data)

    def test_edit_student(self):
        """ Test editing a student's details """
        # Add a student for testing
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, age, grade, subjects) VALUES (?, ?, ?, ?)',
                       ('Kavya Reddy', 23, 'C', 'Biology, Chemistry'))
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()

        # Edit the student's details
        response = self.app.post(f'/students/{student_id}/edit', data={
            'name': 'Kavya Iyer',
            'age': '24',
            'grade': 'B',
            'subjects': 'Biology, Zoology'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after editing

        # Verify the student's details were updated
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()

        self.assertEqual(student[1], 'Kavya Iyer')
        self.assertEqual(student[2], 24)
        self.assertEqual(student[3], 'B')
        self.assertEqual(student[4], 'Biology, Zoology')

    def test_delete_student(self):
        """ Test deleting a student """
        # Add a student for testing
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, age, grade, subjects) VALUES (?, ?, ?, ?)',
                       ('Suresh Patel', 25, 'B', 'Mathematics, Chemistry'))
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()

        # Delete the student
        response = self.app.post(f'/students/{student_id}/delete')
        self.assertEqual(response.status_code, 302)  # Should redirect after deleting

        # Verify the student was deleted
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()

        self.assertIsNone(student)

    def tearDown(self):
        """ Clean up after each test """
        with app.app_context():
            conn = get_db_connection()
            conn.execute('DROP TABLE IF EXISTS students')
            conn.commit()
            conn.close()

if __name__ == '__main__':
    unittest.main()
