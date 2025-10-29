"""
Database migration script to add is_admin column and create admin user
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'vit_switch.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check if is_admin column exists
    cur.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cur.fetchall()]
    
    if 'is_admin' not in columns:
        print("Adding is_admin column to users table...")
        cur.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
        conn.commit()
        print("✓ is_admin column added successfully")
    else:
        print("✓ is_admin column already exists")
    
    # Check if admin user exists
    cur.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
    admin_count = cur.fetchone()[0]
    
    if admin_count == 0:
        print("Creating admin user...")
        cur.execute(
            "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
            ("admin", generate_password_hash("admin123"), 1)
        )
        conn.commit()
        print("✓ Admin user created successfully")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("✓ Admin user already exists")
    
    conn.close()
    print("\nMigration completed successfully!")

if __name__ == '__main__':
    migrate()
