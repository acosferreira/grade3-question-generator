# Deployment Guide

This guide explains how to deploy the Grade 3 Question Generator using **Railway** (backend) and **GitHub Pages** (frontend).

## Architecture Overview

- **Backend (Flask API)**: Deployed on Railway
  - Handles question generation, database operations
  - Provides REST API endpoints
  - Runs on Railway's free tier (500 hours/month)

- **Frontend (Static HTML)**: Deployed on GitHub Pages
  - Static HTML/CSS/JavaScript files in `docs/` folder
  - Connects to Railway backend via API calls
  - Free hosting on GitHub Pages

## Prerequisites

- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))
- Git installed locally

## Step 1: Prepare Your Repository

Your repository is already configured with the necessary files:

- ✅ `Procfile` - Tells Railway how to start the app
- ✅ `railway.json` - Railway configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - Updated with Flask, CORS, and Gunicorn
- ✅ `app.py` - Updated with CORS support
- ✅ `docs/` folder - Static frontend files for GitHub Pages

### Commit and push your changes:

```bash
# Add all changes
git add .

# Commit
git commit -m "Add Railway and GitHub Pages deployment configuration"

# Push to GitHub
git push origin add-ui
```

## Step 2: Deploy Backend to Railway

### 2.1 Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Choose **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account
5. Select your `grade3-question-generator` repository
6. Railway will automatically detect it's a Python app and start building

### 2.2 Monitor Deployment

Railway will:
- Install Python 3.11
- Install dependencies from `requirements.txt`
- Start the app using `gunicorn app:app`

Watch the deployment logs in the Railway dashboard. Wait for it to show "Deployment successful".

### 2.3 Get Your Railway URL

1. In the Railway dashboard, click on your deployment
2. Go to the **"Settings"** tab
3. Scroll to **"Domains"**
4. Click **"Generate Domain"**
5. Railway will create a URL like: `https://your-app-name.up.railway.app`
6. **Copy this URL** - you'll need it in the next step

### 2.4 Test Your Backend

Visit your Railway URL in a browser:
```
https://your-app-name.up.railway.app
```

You should see the Flask app running!

Test an API endpoint:
```
https://your-app-name.up.railway.app/api/questions?subject=all&limit=10
```

## Step 3: Configure Frontend to Use Railway Backend

### 3.1 Update API Configuration

Edit `docs/js/config.js`:

```javascript
// Replace the localhost URL with your Railway URL
const API_BASE_URL = 'https://your-app-name.up.railway.app';
```

**Important:** Remove the trailing slash from your Railway URL!

### 3.2 Commit the Configuration

```bash
# Add the config change
git add docs/js/config.js

# Commit
git commit -m "Configure frontend to use Railway backend"

# Push
git push origin add-ui
```

## Step 4: Deploy Frontend to GitHub Pages

### 4.1 Merge to Master Branch

If you're happy with your changes, merge the `add-ui` branch to `master`:

```bash
# Switch to master
git checkout master

# Merge add-ui branch
git merge add-ui

# Push to GitHub
git push origin master
```

Or create a pull request on GitHub and merge it there.

### 4.2 Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **"Settings"** tab
3. Scroll down to **"Pages"** in the left sidebar
4. Under **"Source"**, select:
   - **Branch:** `master` (or `main`)
   - **Folder:** `/docs`
5. Click **"Save"**

### 4.3 Wait for Deployment

GitHub will build and deploy your site. This takes 1-2 minutes.

Your site will be available at:
```
https://<your-username>.github.io/grade3-question-generator/
```

For example: `https://acosferreira.github.io/grade3-question-generator/`

### 4.4 Test the Frontend

Visit your GitHub Pages URL and test:
- ✅ Home page loads
- ✅ Generate questions works (creates and saves questions)
- ✅ List questions shows saved questions
- ✅ Practice mode works
- ✅ Quiz mode works

## Step 5: Update README (Optional)

Add links to your deployed apps in the README:

```markdown
## Live Demo

- **Frontend (GitHub Pages):** https://your-username.github.io/grade3-question-generator/
- **Backend API (Railway):** https://your-app-name.up.railway.app
```

## Troubleshooting

### Frontend can't connect to backend

**Symptoms:** CORS errors, API calls failing

**Solutions:**
1. Check that `docs/js/config.js` has the correct Railway URL
2. Verify Railway app is running (check Railway dashboard)
3. Check browser console for errors (F12 → Console)
4. Make sure there's no trailing slash in `API_BASE_URL`

### Railway app won't start

**Symptoms:** Build succeeds but app crashes

**Solutions:**
1. Check Railway logs for errors
2. Verify `Procfile` contains: `web: gunicorn app:app`
3. Check that all dependencies are in `requirements.txt`
4. Make sure `runtime.txt` specifies a valid Python version

### GitHub Pages shows 404

**Symptoms:** Page not found on GitHub Pages URL

**Solutions:**
1. Wait 2-3 minutes after enabling GitHub Pages
2. Verify `/docs` folder is on the master/main branch
3. Check GitHub Actions tab for build errors
4. Make sure `index.html` exists in `/docs` folder

### Questions not persisting

**Symptoms:** Generated questions disappear after restart

**Railway Note:** The free tier doesn't have persistent storage. Your SQLite database will reset when the app restarts. To get persistence, you can:
1. Upgrade to Railway Pro (includes persistent volumes)
2. Use a PostgreSQL database instead of SQLite
3. Accept that questions are temporary on the free tier

To add PostgreSQL (optional):
1. In Railway dashboard, click "+ New"
2. Select "PostgreSQL"
3. Update `database.py` to use PostgreSQL instead of SQLite

## Environment Variables (Optional)

You can add environment variables in Railway:

1. Go to Railway dashboard
2. Click on your app
3. Go to "Variables" tab
4. Add variables:
   - `SECRET_KEY`: A random secret key for Flask sessions
   - `LLAMA_URL`: URL for Ollama/LLM service (if using)

## Cost Breakdown

### Current Setup (FREE)

- **Railway Free Tier:**
  - 500 hours/month (about 16 hours/day)
  - $0.000231/GB-hour for usage
  - $5 monthly credit
  - Perfect for personal/low-traffic use

- **GitHub Pages:**
  - Completely free
  - 100 GB bandwidth/month
  - No usage limits for public repos

### If You Need More

If you exceed Railway's free tier:

**Alternative backends (all with free tiers):**
- **Render** - Free tier spins down after 15 min inactivity
- **PythonAnywhere** - Free tier always-on but limited CPU
- **Fly.io** - Free tier with 3 VMs
- **Vercel** - Free tier for serverless Python

## Monitoring

### Railway Metrics

Railway provides:
- Deployment logs
- Resource usage graphs
- Request metrics
- Error tracking

Access these in your Railway dashboard.

### Analytics (Optional)

Add Google Analytics to your frontend:

1. Get a Google Analytics tracking ID
2. Add tracking code to all HTML files in `docs/`
3. Monitor traffic and usage

## Maintenance

### Updating the Backend

```bash
# Make changes to Python files
# Commit and push
git add .
git commit -m "Update backend"
git push origin master

# Railway auto-deploys from GitHub
```

### Updating the Frontend

```bash
# Make changes to docs/ files
# Commit and push
git add docs/
git commit -m "Update frontend"
git push origin master

# GitHub Pages auto-deploys
```

## Security Notes

1. **Never commit secrets** - Use Railway environment variables
2. **CORS is enabled** - Only allow your GitHub Pages domain in production
3. **API rate limiting** - Consider adding rate limiting to prevent abuse
4. **Input validation** - Flask app validates all inputs

## Support

If you need help:

- **Railway:** https://railway.app/help
- **GitHub Pages:** https://docs.github.com/pages
- **This project:** Open an issue on GitHub

---

**Congratulations!** 🎉 Your Grade 3 Question Generator is now live!

- Students can access it at: `https://your-username.github.io/grade3-question-generator/`
- Share the link with students, parents, or teachers
- No installation required - works in any modern browser
