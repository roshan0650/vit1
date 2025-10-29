"""
Add sample data to the database for testing
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'vit_switch.db')

def add_sample_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check if there's already data
    cur.execute("SELECT COUNT(*) FROM faculty_reviews")
    if cur.fetchone()[0] > 0:
        print("Sample data already exists. Skipping...")
        conn.close()
        return
    
    print("Adding sample data...")
    
    # Get student user id
    cur.execute("SELECT id FROM users WHERE username='student'")
    user_result = cur.fetchone()
    if not user_result:
        print("Student user not found. Please create a student account first.")
        conn.close()
        return
    
    student_id = user_result[0]
    
    # Add faculty reviews
    faculty_reviews = [
        (student_id, '21BCE1234', '2nd Year', 'CSE', 'Dr. Smith', 'Excellent teaching style, very clear explanations.', datetime.utcnow().isoformat()),
        (student_id, '21BCE1234', '2nd Year', 'CSE', 'Prof. Johnson', 'Good professor but assignments are very tough.', datetime.utcnow().isoformat()),
        (student_id, '21BCE1234', '2nd Year', 'CSE', 'Dr. Williams', 'Very helpful during office hours.', datetime.utcnow().isoformat()),
    ]
    
    cur.executemany(
        "INSERT INTO faculty_reviews (user_id, roll_no, current_year, branch, faculty, review_text, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        faculty_reviews
    )
    
    # Add course reviews
    course_reviews = [
        (student_id, '21BCE1234', '2nd Year', 'Data Structures', 'Very interesting course with practical applications.', datetime.utcnow().isoformat()),
        (student_id, '21BCE1234', '2nd Year', 'Operating Systems', 'Challenging but rewarding course.', datetime.utcnow().isoformat()),
        (student_id, '21BCE1234', '2nd Year', 'Database Management', 'Well structured course with good projects.', datetime.utcnow().isoformat()),
    ]
    
    cur.executemany(
        "INSERT INTO course_reviews (user_id, roll_no, current_year, course, review_text, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        course_reviews
    )
    
    # Add batch requests
    batch_requests = [
        (student_id, 'Batch A1', 'Batch B2', 8.5, '8.0-9.0', 'Review Pending', datetime.utcnow().isoformat()),
        (student_id, 'Batch C3', 'Batch A1', 9.2, '9.0-10.0', 'Review Pending', datetime.utcnow().isoformat()),
    ]
    
    cur.executemany(
        "INSERT INTO batch_requests (user_id, current_batch, preferred_batch, current_cgpa, preferred_cgpa_range, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        batch_requests
    )
    
    conn.commit()
    conn.close()
    
    print("✓ Sample data added successfully!")
    print("  - 3 Faculty Reviews")
    print("  - 3 Course Reviews")
    print("  - 2 Batch Switch Requests")

if __name__ == '__main__':
    add_sample_data()
