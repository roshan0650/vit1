# VIT Switch - Complete Full-Stack Application

A professional, youth-centric web application for VIT students built with Flask and SQLite.

## Features Implemented

### Backend & Database
- **Flask Backend** with session management and authentication
- **SQLite Database** with 4 tables:
  - `users` - User authentication (hashed passwords)
  - `faculty_reviews` - Faculty review submissions
  - `course_reviews` - Course review submissions  
  - `batch_requests` - Batch switch requests with status tracking

### Frontend Pages
1. **Login Page** - Secure authentication
2. **Home Page** - Auto-popup modal with 3 options (bottom-to-center animation)
3. **Reviews Menu** - Modal with Faculty Review & Course Review options
4. **Faculty Review Form** - Roll no, year, branch, faculty, review (1000 word limit)
5. **Course Review Form** - Roll no, year, course, review (1000 word limit)
6. **Batch Switch Form** - Current/preferred batch, CGPA, CGPA range
7. **Eduvids** - Course selector (CSE/CSM/CSD/CSIT) with YouTube video links
8. **Dashboard** - Recent submissions overview
9. **Success Pages** - Confirmation after submissions

### Functionality
- All forms submit to backend and save to SQLite database
- Cancel buttons return to home page
- Submit buttons save data and show success messages
- Back functionality on all pages
- Word count validation (1000 words max) on review forms
- YouTube video recommendations redirect to actual videos
- User dashboard shows recent activity
- Logout functionality with session clearing

## Running the Application

### Already Running!
The server is currently live at: **http://127.0.0.1:5000**

### Login Credentials
- Username: `student`
- Password: `password`

### Manual Start (if needed)
```powershell
# Activate virtual environment
.\.venv\Scripts\activate

# Run the application
python app.py
```

## Project Structure
```
vit-switch/
├── app.py                    # Flask backend with all routes
├── vit_switch.db             # SQLite database (auto-created)
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
│   ├── base.html            # Base template with header/nav
│   ├── login.html           # Login page
│   ├── home.html            # Home with options modal
│   ├── reviews_menu.html    # Review type selection
│   ├── faculty_review.html  # Faculty review form
│   ├── course_review.html   # Course review form
│   ├── batch_switch.html    # Batch switch form
│   ├── eduvids.html         # Educational videos page
│   ├── dashboard.html       # User dashboard
│   ├── submit_success.html  # Success confirmation
│   └── request_sent.html    # Batch request confirmation
└── static/
    ├── css/
    │   └── style.css        # Minimal professional styling (#03045e)
    └── js/
        └── app.js           # Modal controls, validation, navigation

```

## Database Schema

### users table
- id (PRIMARY KEY)
- username (UNIQUE)
- password_hash (bcrypt hashed)

### faculty_reviews table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- roll_no
- current_year
- branch
- faculty
- review_text
- created_at

### course_reviews table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- roll_no
- current_year
- course
- review_text
- created_at

### batch_requests table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- current_batch
- preferred_batch
- current_cgpa
- preferred_cgpa_range
- status
- created_at

## Tech Stack
- **Backend**: Flask 3.0.3
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Auth**: Flask sessions with Werkzeug password hashing
- **Styling**: Custom CSS with #03045e color palette

## Design Philosophy
- Simple and professional (no AI-looking fancy animations)
- Youth-centric but minimal
- Clean forms with proper validation
- Mobile-responsive layout
- Inspired by kollegio.ai but kept basic

## Next Steps (Optional Enhancements)
- Add user registration
- Admin panel to review batch requests
- Export reviews to CSV
- Email notifications
- Profile picture uploads
- Advanced search/filter on dashboard
