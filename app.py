from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("VIT_SWITCH_SECRET", "dev-secret-key")
DB_PATH = os.path.join(os.path.dirname(__file__), 'vit_switch.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS faculty_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            roll_no TEXT,
            current_year TEXT,
            branch TEXT,
            faculty TEXT,
            review_text TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            roll_no TEXT,
            current_year TEXT,
            course TEXT,
            review_text TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS batch_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            current_batch TEXT,
            preferred_batch TEXT,
            current_cgpa REAL,
            preferred_cgpa_range TEXT,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    # Seed a default user if none exists
    cur.execute("SELECT COUNT(*) as c FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
            ("student", generate_password_hash("password"), 0)
        )
    # Seed admin user
    cur.execute("SELECT COUNT(*) as c FROM users WHERE is_admin=1")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
            ("admin", generate_password_hash("admin123"), 1)
        )
    conn.commit()
    conn.close()


with app.app_context():
    init_db()


def login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)

    return wrapped


def admin_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('home'))
        return view_func(*args, **kwargs)

    return wrapped


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        conn.close()
        if row and check_password_hash(row['password_hash'], password):
            session['user_id'] = row['id']
            session['username'] = row['username']
            session['is_admin'] = bool(row['is_admin'])
            return redirect(url_for('home'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/reviews')
@login_required
def reviews_menu():
    return render_template('reviews_menu.html')


@app.route('/reviews/faculty', methods=['GET', 'POST'])
@login_required
def faculty_review():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        current_year = request.form.get('current_year')
        branch = request.form.get('branch')
        faculty = request.form.get('faculty')
        review_text = request.form.get('review_text')[:6000]
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO faculty_reviews (user_id, roll_no, current_year, branch, faculty, review_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (session['user_id'], roll_no, current_year, branch, faculty, review_text, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
        return redirect(url_for('submitted', msg='successfully submitted'))
    return render_template('faculty_review.html')


@app.route('/reviews/course', methods=['GET', 'POST'])
@login_required
def course_review():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        current_year = request.form.get('current_year')
        course = request.form.get('course')
        review_text = request.form.get('review_text')[:6000]
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO course_reviews (user_id, roll_no, current_year, course, review_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (session['user_id'], roll_no, current_year, course, review_text, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
        return redirect(url_for('submitted', msg='successfully submitted'))
    return render_template('course_review.html')


@app.route('/submitted')
@login_required
def submitted():
    msg = request.args.get('msg', 'successfully submitted')
    return render_template('submit_success.html', message=msg)


@app.route('/batch-switch', methods=['GET', 'POST'])
@login_required
def batch_switch():
    if request.method == 'POST':
        current_batch = request.form.get('current_batch')
        preferred_batch = request.form.get('preferred_batch')
        current_cgpa = request.form.get('current_cgpa')
        preferred_cgpa_range = request.form.get('preferred_cgpa_range')
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO batch_requests (user_id, current_batch, preferred_batch, current_cgpa, preferred_cgpa_range, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (session['user_id'], current_batch, preferred_batch, current_cgpa, preferred_cgpa_range, 'Review Pending', datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
        return redirect(url_for('request_sent'))
    return render_template('batch_switch.html')


@app.route('/request-sent')
@login_required
def request_sent():
    msg = "request sent for review, we will reach out to you asap"
    return render_template('request_sent.html', message=msg)


@app.route('/eduvids', methods=['GET', 'POST'])
@login_required
def eduvids():
    videos = []
    selected = None
    if request.method == 'POST':
        selected = request.form.get('course')
        videos = get_videos_for_course(selected)
    return render_template('eduvids.html', selected=selected, videos=videos)


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM faculty_reviews WHERE user_id=? ORDER BY created_at DESC LIMIT 5", (session['user_id'],))
    faculty_items = cur.fetchall()
    cur.execute("SELECT * FROM course_reviews WHERE user_id=? ORDER BY created_at DESC LIMIT 5", (session['user_id'],))
    course_items = cur.fetchall()
    cur.execute("SELECT * FROM batch_requests WHERE user_id=? ORDER BY created_at DESC LIMIT 5", (session['user_id'],))
    batch_items = cur.fetchall()
    conn.close()
    return render_template('dashboard.html', faculty_items=faculty_items, course_items=course_items, batch_items=batch_items)


def get_videos_for_course(course):
    mapping = {
        'cse': [
            ('Data Structures Roadmap', 'https://www.youtube.com/watch?v=RBSGKlAvoiM'),
            ('Operating Systems Basics', 'https://www.youtube.com/watch?v=vBURTt97EkA'),
            ('DBMS Crash Course', 'https://www.youtube.com/watch?v=HXV3zeQKqGY')
        ],
        'csm': [
            ('Machine Learning Intro', 'https://www.youtube.com/watch?v=GwIo3gDZCVQ'),
            ('Probability for ML', 'https://www.youtube.com/watch?v=YXLVjCKVP7Q'),
            ('Python for ML', 'https://www.youtube.com/watch?v=_uQrJ0TkZlc')
        ],
        'csd': [
            ('System Design Primer', 'https://www.youtube.com/watch?v=zXfS4YMGzNU'),
            ('Scalability Basics', 'https://www.youtube.com/watch?v=-W9F__D3oY4'),
            ('Design Patterns', 'https://www.youtube.com/watch?v=NU_1StN5Tkk')
        ],
        'csit': [
            ('Networking Fundamentals', 'https://www.youtube.com/watch?v=qiQR5rTSshw'),
            ('Cloud Basics', 'https://www.youtube.com/watch?v=2LaAJq1lB1Q'),
            ('Linux Basics', 'https://www.youtube.com/watch?v=iwolPf6kN-k')
        ]
    }
    return mapping.get((course or '').lower(), [])


@app.route('/admin')
@admin_required
def admin_panel():
    return render_template('admin_panel.html')


@app.route('/admin/faculty-reviews')
@admin_required
def admin_faculty_reviews():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT fr.*, u.username 
        FROM faculty_reviews fr 
        LEFT JOIN users u ON fr.user_id = u.id 
        ORDER BY fr.created_at DESC
    """)
    reviews = cur.fetchall()
    conn.close()
    return render_template('admin_faculty_reviews.html', reviews=reviews)


@app.route('/admin/course-reviews')
@admin_required
def admin_course_reviews():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT cr.*, u.username 
        FROM course_reviews cr 
        LEFT JOIN users u ON cr.user_id = u.id 
        ORDER BY cr.created_at DESC
    """)
    reviews = cur.fetchall()
    conn.close()
    return render_template('admin_course_reviews.html', reviews=reviews)


@app.route('/admin/batch-requests')
@admin_required
def admin_batch_requests():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT br.*, u.username 
        FROM batch_requests br 
        LEFT JOIN users u ON br.user_id = u.id 
        ORDER BY br.created_at DESC
    """)
    requests = cur.fetchall()
    conn.close()
    return render_template('admin_batch_requests.html', requests=requests)


@app.route('/admin/batch-request/<int:request_id>/update', methods=['POST'])
@admin_required
def update_batch_request(request_id):
    status = request.form.get('status')
    if status not in ['Approved', 'Rejected', 'Review Pending']:
        flash('Invalid status', 'error')
        return redirect(url_for('admin_batch_requests'))
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE batch_requests SET status=? WHERE id=?",
        (status, request_id)
    )
    conn.commit()
    conn.close()
    flash(f'Request {status.lower()} successfully', 'success')
    return redirect(url_for('admin_batch_requests'))


@app.route('/admin/delete/faculty-review/<int:review_id>', methods=['POST'])
@admin_required
def delete_faculty_review(review_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM faculty_reviews WHERE id=?", (review_id,))
    conn.commit()
    conn.close()
    flash('Faculty review deleted successfully', 'success')
    return redirect(url_for('admin_faculty_reviews'))


@app.route('/admin/delete/course-review/<int:review_id>', methods=['POST'])
@admin_required
def delete_course_review(review_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM course_reviews WHERE id=?", (review_id,))
    conn.commit()
    conn.close()
    flash('Course review deleted successfully', 'success')
    return redirect(url_for('admin_course_reviews'))


@app.route('/admin/stats')
@admin_required
def admin_stats():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM users WHERE is_admin=0")
    total_users = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM faculty_reviews")
    total_faculty_reviews = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM course_reviews")
    total_course_reviews = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM batch_requests")
    total_batch_requests = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM batch_requests WHERE status='Review Pending'")
    pending_requests = cur.fetchone()[0]
    
    conn.close()
    
    stats = {
        'total_users': total_users,
        'total_faculty_reviews': total_faculty_reviews,
        'total_course_reviews': total_course_reviews,
        'total_batch_requests': total_batch_requests,
        'pending_requests': pending_requests
    }
    
    return render_template('admin_stats.html', stats=stats)


if __name__ == '__main__':
    app.run(debug=True)
