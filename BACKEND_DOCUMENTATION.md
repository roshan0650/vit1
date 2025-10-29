# VIT Switch - Backend & Database Documentation

## Complete Backend Implementation

### Database: SQLite3 (`vit_switch.db`)

**Status**: ✅ Fully Functional & Tested

#### Tables Schema

**1. users**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
```
- Stores user authentication data
- Passwords hashed using Werkzeug's `generate_password_hash()`
- Default user: `student` / `password`

**2. faculty_reviews**
```sql
CREATE TABLE faculty_reviews (
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
```
- Stores faculty reviews submitted by students
- Foreign key relationship with users table
- Timestamps in ISO format

**3. course_reviews**
```sql
CREATE TABLE course_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    roll_no TEXT,
    current_year TEXT,
    course TEXT,
    review_text TEXT,
    created_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```
- Stores course reviews submitted by students
- Foreign key relationship with users table
- Timestamps in ISO format

**4. batch_requests**
```sql
CREATE TABLE batch_requests (
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
```
- Stores batch switch requests
- Includes CGPA data and status tracking
- Status field for admin workflow (default: "Review Pending")

---

## Flask Backend Routes

### Authentication Routes

**`GET /` or `POST /`** (login)
- **Template**: `login.html`
- **Method**: GET displays form, POST processes login
- **POST Data**: `username`, `password`
- **Backend Logic**:
  - Queries users table for username
  - Verifies password hash using `check_password_hash()`
  - Sets session variables: `user_id`, `username`
  - Redirects to `/home` on success
  - Flashes error message on failure

**`GET /logout`**
- **Protected**: Requires login
- **Backend Logic**:
  - Clears session data with `session.clear()`
  - Redirects to login page

---

### Main Application Routes

**`GET /home`**
- **Protected**: Requires login
- **Template**: `home.html`
- **Features**: Shows modal with 3 options (Reviews, Batch Switch, Eduvids)

**`GET /reviews`**
- **Protected**: Requires login
- **Template**: `reviews_menu.html`
- **Features**: Shows modal with Faculty Review and Course Review options

---

### Review Routes

**`GET /reviews/faculty` or `POST /reviews/faculty`**
- **Protected**: Requires login
- **Template**: `faculty_review.html`
- **POST Data**: `roll_no`, `current_year`, `branch`, `faculty`, `review_text`
- **Backend Logic**:
  - Truncates review_text to 6000 characters (server-side protection)
  - Inserts into `faculty_reviews` table with timestamp
  - Includes `user_id` from session
  - Commits to database
  - Redirects to `/submitted` success page

**`GET /reviews/course` or `POST /reviews/course`**
- **Protected**: Requires login
- **Template**: `course_review.html`
- **POST Data**: `roll_no`, `current_year`, `course`, `review_text`
- **Backend Logic**:
  - Truncates review_text to 6000 characters
  - Inserts into `course_reviews` table with timestamp
  - Includes `user_id` from session
  - Commits to database
  - Redirects to `/submitted` success page

**`GET /submitted`**
- **Protected**: Requires login
- **Template**: `submit_success.html`
- **Query Param**: `msg` (optional message to display)

---

### Batch Switch Routes

**`GET /batch-switch` or `POST /batch-switch`**
- **Protected**: Requires login
- **Template**: `batch_switch.html`
- **POST Data**: `current_batch`, `preferred_batch`, `current_cgpa`, `preferred_cgpa_range`
- **Backend Logic**:
  - Inserts into `batch_requests` table
  - Sets status to "Review Pending"
  - Includes timestamp and `user_id`
  - Commits to database
  - Redirects to `/request-sent` confirmation page

**`GET /request-sent`**
- **Protected**: Requires login
- **Template**: `request_sent.html`
- **Message**: "request sent for review, we will reach out to you asap"

---

### Eduvids Routes

**`GET /eduvids` or `POST /eduvids`**
- **Protected**: Requires login
- **Template**: `eduvids.html`
- **POST Data**: `course` (cse/csm/csd/csit)
- **Backend Logic**:
  - Calls `get_videos_for_course()` helper function
  - Returns course-specific YouTube video recommendations
  - Videos data hardcoded but can be extended with database
  - Renders template with video list

**Helper Function**: `get_videos_for_course(course)`
```python
Returns list of tuples: [(title, youtube_url), ...]
Mappings:
- CSE: Data Structures, Operating Systems, DBMS
- CSM: Machine Learning, Probability, Python for ML
- CSD: System Design, Scalability, Design Patterns
- CSIT: Networking, Cloud, Linux
```

---

### Dashboard Routes

**`GET /dashboard`**
- **Protected**: Requires login
- **Template**: `dashboard.html`
- **Backend Logic**:
  - Queries latest 5 faculty_reviews for current user
  - Queries latest 5 course_reviews for current user
  - Queries latest 5 batch_requests for current user
  - Orders by `created_at DESC`
  - Passes all data to template for display

---

## Security Features

### 1. Authentication
- Session-based authentication using Flask sessions
- Secure session cookies with secret key
- Password hashing with Werkzeug (scrypt algorithm)

### 2. Authorization
- `@login_required` decorator on all protected routes
- Redirects to login if session is missing `user_id`
- Prevents unauthorized access to application pages

### 3. Data Validation
- Server-side truncation of review text (6000 chars max)
- Client-side word count validation (1000 words)
- Required field validation on all forms
- CGPA input validation (0-10 range, step 0.01)

### 4. SQL Injection Protection
- Parameterized queries using `?` placeholders
- SQLite3 Row factory for safe data access
- No raw SQL string concatenation

---

## Database Helper Functions

**`get_db()`**
- Creates new SQLite connection
- Sets row_factory to sqlite3.Row for dict-like access
- Returns connection object

**`init_db()`**
- Creates all tables if they don't exist
- Seeds default user if users table is empty
- Called on application startup via `app.app_context()`

---

## Testing & Verification

### Included Test Scripts

**`inspect_db.py`**
- Inspects database structure
- Shows table schemas
- Displays row counts
- Shows sample data (first 3 rows per table)

**`test_backend.py`**
- Inserts test data for all features
- Verifies database operations
- Shows confirmation of successful inserts
- Demonstrates backend functionality

### Run Tests
```powershell
# Inspect database
python inspect_db.py

# Test backend operations
python test_backend.py
```

---

## Current Status

✅ **Database**: Created and initialized with schema  
✅ **Tables**: 4 tables (users, faculty_reviews, course_reviews, batch_requests)  
✅ **Routes**: 11 routes fully implemented  
✅ **Authentication**: Session-based auth with password hashing  
✅ **Data Persistence**: All forms save to SQLite  
✅ **Test Data**: Sample data inserted successfully  
✅ **Server**: Running on http://127.0.0.1:5000  

## Test Results

```
Total users: 1
Total faculty reviews: 1
Total course reviews: 1
Total batch requests: 1
```

**Sample Faculty Review:**
- Faculty: Dr. Sharma
- Branch: Computer Science
- Status: Stored in database ✅

**Sample Course Review:**
- Course: Data Structures and Algorithms
- Year: 3rd Year
- Status: Stored in database ✅

**Sample Batch Request:**
- From Batch A1 → To Batch B2
- CGPA: 8.5
- Status: Review Pending ✅

---

## Technology Stack

- **Backend Framework**: Flask 3.0.3
- **Database**: SQLite3 (file-based, no separate server needed)
- **ORM**: None (raw SQL with parameterized queries)
- **Auth**: Flask sessions + Werkzeug password hashing
- **Validation**: Server-side + client-side (JavaScript)

---

## Next Steps (Optional)

1. **Admin Panel**: Create routes to approve/reject batch requests
2. **User Registration**: Add signup functionality
3. **Email Notifications**: Send emails on batch request updates
4. **Search/Filter**: Add search on dashboard
5. **Export**: CSV export for reviews
6. **Analytics**: Dashboard statistics and charts
7. **File Uploads**: Add support for document attachments
8. **REST API**: Create JSON API endpoints for mobile app
