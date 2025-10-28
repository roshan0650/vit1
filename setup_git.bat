@echo off
echo ============================================
echo VIT SWITCH - Git Setup
echo ============================================
echo.

cd /d "%~dp0"

echo Setting up git user (you can change this later)...
git config user.name "VIT Student"
git config user.email "student@vit.edu"

echo.
echo Creating initial commit...
git commit -m "Initial commit"

echo.
echo ============================================
echo Git repository is ready!
echo ============================================
echo.
echo Next steps:
echo 1. Create a GitHub repository at https://github.com/new
echo 2. Name it: vit-switch
echo 3. Run these commands (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/vit-switch.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo Then deploy to Railway: https://railway.app
echo.
pause
