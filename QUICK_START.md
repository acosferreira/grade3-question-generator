# Quick Start - Deploy in 10 Minutes

This is a simplified guide to get your app live quickly.

## Prerequisites
- GitHub account (free)
- Railway account at [railway.app](https://railway.app) (free)

## Step 1: Push to GitHub (2 minutes)

```bash
# Commit all changes
git add .
git commit -m "Add deployment configuration"

# If not on master, merge your branch
git checkout master
git merge add-ui

# Push to GitHub
git push origin master
```

## Step 2: Deploy Backend to Railway (3 minutes)

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select `grade3-question-generator`
4. Wait for deployment (1-2 minutes)
5. Click **Settings** → **Generate Domain**
6. **Copy your URL** (e.g., `https://xyz.up.railway.app`)

## Step 3: Update Frontend Config (1 minute)

Edit `docs/js/config.js`:

```javascript
const API_BASE_URL = 'https://your-railway-url.up.railway.app';  // Paste your Railway URL here
```

Commit and push:

```bash
git add docs/js/config.js
git commit -m "Configure Railway backend URL"
git push origin master
```

## Step 4: Enable GitHub Pages (2 minutes)

1. Go to your GitHub repo → **Settings** → **Pages**
2. Under "Source":
   - Branch: `master`
   - Folder: `/docs`
3. Click **Save**
4. Wait 1-2 minutes

## Step 5: Test Your App (2 minutes)

Your app is live at:
```
https://YOUR-USERNAME.github.io/grade3-question-generator/
```

Test it:
1. Visit the URL
2. Click "Generate Questions"
3. Generate 5 math questions
4. Go to "List" to see them saved
5. Try "Quiz Mode"

## Done! 🎉

You now have:
- ✅ Backend API on Railway (free 500 hours/month)
- ✅ Frontend on GitHub Pages (free forever)
- ✅ Full question generator app
- ✅ No servers to maintain

## Sharing Your App

Send this link to anyone:
```
https://YOUR-USERNAME.github.io/grade3-question-generator/
```

They can use it directly in their browser - no installation needed!

## Troubleshooting

**"Error connecting to backend"**
- Check Railway app is running (green status in dashboard)
- Verify URL in `docs/js/config.js` matches your Railway domain
- Check for typos (no trailing slash!)

**"404 Not Found on GitHub Pages"**
- Wait 2-3 minutes for GitHub Pages to deploy
- Check GitHub Actions tab for build status
- Verify `/docs` folder exists on master branch

## Need More Help?

See the full [DEPLOYMENT.md](DEPLOYMENT.md) guide for detailed instructions and troubleshooting.
