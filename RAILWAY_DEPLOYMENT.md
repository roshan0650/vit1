# Deploy VIT Switch to Railway

## Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app)

## Deployment Steps

### Step 1: Initialize Git Repository

```powershell
# Navigate to project directory
cd C:\Users\Munni\CascadeProjects\vit-switch

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - VIT Switch Flask app"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `vit-switch`
3. Keep it **Public** or **Private** (your choice)
4. Do NOT initialize with README (we already have files)
5. Click "Create repository"

### Step 3: Push to GitHub

Copy the commands from GitHub, or use:

```powershell
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/vit-switch.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Railway

1. **Go to Railway**: https://railway.app
2. **Sign in** with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your **`vit-switch`** repository
6. Railway will automatically detect Flask and deploy!

### Step 5: Configure Environment Variable (Optional but Recommended)

1. Click on your deployed project
2. Go to **"Variables"** tab
3. Add new variable:
   - Key: `VIT_SWITCH_SECRET`
   - Value: (generate random string, e.g., `your-super-secret-key-here-xyz123`)
4. Click "Save"

### Step 6: Get Your URL

1. Go to **"Settings"** tab
2. Click **"Generate Domain"**
3. Your app will be live at: `your-app-name.up.railway.app`

## What Railway Does Automatically

✅ Detects Python app  
✅ Installs dependencies from `requirements.txt`  
✅ Runs database initialization on first start  
✅ Starts gunicorn server  
✅ Creates HTTPS certificate  
✅ Provides custom domain  

## Files Created for Deployment

- `railway.json` - Railway configuration
- `Procfile` - Process command
- `runtime.txt` - Python version
- `.gitignore` - Files to exclude from git
- `.railwayignore` - Files to exclude from deployment
- Updated `requirements.txt` - Added gunicorn

## Default User After Deployment

The app will create a default user on first run:
- **Username**: `student`
- **Password**: `password`

**⚠️ IMPORTANT**: After deployment, login and change default credentials!

## Database Persistence

Railway provides **persistent storage** for your SQLite database.
- Database file: `vit_switch.db`
- Data persists across deployments
- Automatic backups available in Railway dashboard

## Monitoring

In Railway dashboard:
- View **Logs** for debugging
- Check **Metrics** (CPU, Memory, Bandwidth)
- See **Deployments** history
- Configure **Custom Domain**

## Troubleshooting

### Deployment Failed?
- Check Railway logs in dashboard
- Verify all files are committed to GitHub
- Make sure `requirements.txt` includes gunicorn

### Database Not Working?
- Railway creates the database on first run
- Check logs for errors during `init_db()`
- Database is stored in persistent volume

### App Not Loading?
- Wait 1-2 minutes after deployment
- Check if service is running in Railway dashboard
- Verify no errors in logs

## Cost

- **Free Tier**: $5 worth of usage per month
- **Hobby Plan**: $5/month for more resources
- **Pro Plan**: Custom pricing

Your VIT Switch app should run comfortably on the free tier!

## Update Deployment

To update your app after changes:

```powershell
git add .
git commit -m "Update description"
git push
```

Railway automatically redeploys on push!

## Custom Domain (Optional)

1. In Railway dashboard, go to **Settings**
2. Click **"Custom Domain"**
3. Add your domain (e.g., `vitswitch.com`)
4. Follow DNS configuration instructions
5. Railway handles SSL automatically

## Security Notes

- Railway uses HTTPS automatically
- Set strong `VIT_SWITCH_SECRET` environment variable
- Consider changing default user password
- Database is isolated per deployment

## Need Help?

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Create issue in your repo

---

**Your app is ready to deploy! Follow the steps above to get it live on Railway.** 🚀
