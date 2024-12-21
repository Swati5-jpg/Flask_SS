import sqlite3

def create_table():
    # Connect to SQLite database (creates students.db if it doesn't exist)
    conn = sqlite3.connect('students.db')

    # Create the students table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL,
        subjects TEXT NOT NULL
    )
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Table 'students' created successfully!")

if __name__ == "__main__":
    create_table()
