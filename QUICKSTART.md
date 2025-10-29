# VIT Switch - Quick Start Guide

## 🚀 Your App is LIVE!

**URL**: http://127.0.0.1:5000

## 📝 Login Credentials

```
Username: student
Password: password
```

## ✅ What's Already Working

### 1. Complete Database Backend
- ✅ SQLite database created (`vit_switch.db`)
- ✅ 4 tables with proper relationships
- ✅ Sample data inserted for testing
- ✅ All CRUD operations functional

### 2. Flask Backend Server
- ✅ Running on http://127.0.0.1:5000
- ✅ 11 routes fully implemented
- ✅ Session-based authentication
- ✅ Password hashing (secure)
- ✅ Form validation (client + server)

### 3. Frontend Pages
- ✅ Login page
- ✅ Home with auto-popup modal (3 options)
- ✅ Reviews menu (2 options)
- ✅ Faculty review form
- ✅ Course review form
- ✅ Batch switch form
- ✅ Eduvids with course selector
- ✅ User dashboard
- ✅ Success/confirmation pages
- ✅ Logout functionality

### 4. Features
- ✅ Bottom-to-center animations on modals
- ✅ Back button on all pages
- ✅ Cancel buttons (return to home)
- ✅ Submit buttons (save to database)
- ✅ Word count validation (1000 words)
- ✅ YouTube video links (open in new tab)
- ✅ Professional styling (#03045e palette)
- ✅ Mobile responsive

## 🎯 How to Use

### Step 1: Login
1. Open http://127.0.0.1:5000
2. Enter username: `student`
3. Enter password: `password`
4. Click Login

### Step 2: Choose an Option
Modal will auto-popup with 3 options:
- **Reviews** → Faculty or Course reviews
- **Batch Switch** → Request batch change
- **Eduvids** → Get course videos

### Step 3: Submit Reviews
**Faculty Review:**
1. Click Reviews → Faculty Review
2. Fill: Roll No, Year, Branch, Faculty Name
3. Write review (max 1000 words)
4. Click Submit or Cancel

**Course Review:**
1. Click Reviews → Course Review
2. Fill: Roll No, Year, Course Name
3. Write review (max 1000 words)
4. Click Submit or Cancel

### Step 4: Request Batch Switch
1. Click Batch Switch
2. Fill: Current batch, Preferred batch
3. Enter: Current CGPA, Preferred CGPA range
4. Click Submit or Cancel

### Step 5: Browse Eduvids
1. Click Eduvids
2. Select course: CSE, CSM, CSD, or CSIT
3. Click "Get Videos"
4. Click any video to open on YouTube

### Step 6: Check Dashboard
1. Click "Dashboard" in header
2. View your recent submissions:
   - Faculty reviews
   - Course reviews
   - Batch switch requests

### Step 7: Logout
1. Click "Logout" in header
2. Returns to login page

## 🔧 Management Commands

### Inspect Database
```powershell
python inspect_db.py
```
Shows all tables, schemas, and data

### Test Backend
```powershell
python test_backend.py
```
Inserts sample data and verifies operations

### Start Server (if stopped)
```powershell
python app.py
```

### Stop Server
Press `CTRL+C` in terminal

## 📁 Project Files

```
vit-switch/
├── app.py                          # Main Flask application
├── vit_switch.db                   # SQLite database (auto-created)
├── requirements.txt                # Python dependencies
├── README.md                       # Full documentation
├── BACKEND_DOCUMENTATION.md        # Backend API docs
├── QUICKSTART.md                   # This file
├── inspect_db.py                   # Database inspection tool
├── test_backend.py                 # Backend testing script
├── templates/                      # HTML templates (12 files)
└── static/
    ├── css/style.css              # Styling
    └── js/app.js                  # JavaScript
```

## 🎨 Color Palette

Primary: `#03045e` (Deep Blue)
- Reflects the youth-centric, professional vibe
- Used in header, buttons, and links
- Inspired by modern education platforms

## 🔐 Security Features

✅ Password hashing (scrypt algorithm)  
✅ Session-based authentication  
✅ SQL injection protection (parameterized queries)  
✅ Client + server validation  
✅ CSRF protection (Flask built-in)

## 📊 Database Stats

After running `test_backend.py`:
- Users: 1
- Faculty Reviews: 1
- Course Reviews: 1
- Batch Requests: 1

## 🎬 Demo Flow

1. **Login** → Auto-popup with 3 options
2. **Click Reviews** → Choose Faculty or Course
3. **Fill Form** → All fields required
4. **Submit** → Data saved to database
5. **Success Page** → Confirmation message
6. **Dashboard** → View all your submissions
7. **Eduvids** → Select course, get videos
8. **Logout** → Return to login

## 💡 Tips

- Use Back button to navigate previous pages
- Use Cancel to return to home without saving
- Dashboard shows your latest 5 submissions per category
- All YouTube links open in new tab
- Word counter validates before submission

## 🐛 Troubleshooting

**Server not running?**
```powershell
python app.py
```

**Database locked?**
Close any database browser tools and restart server

**Port 5000 in use?**
Edit `app.py`, change last line to:
```python
app.run(debug=True, port=5001)
```

## 📞 Support

All features are fully functional. The application:
- ✅ Accepts form submissions
- ✅ Stores data in SQLite
- ✅ Validates input
- ✅ Shows confirmation pages
- ✅ Displays dashboard data
- ✅ Links to YouTube videos
- ✅ Handles navigation and routing

**Everything is working and ready to use!**
