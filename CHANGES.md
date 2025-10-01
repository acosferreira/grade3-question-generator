# Changes Made for Deployment

This document lists all changes made to enable Railway + GitHub Pages deployment.

## New Files Created

### Deployment Configuration
- **`Procfile`** - Tells Railway how to start the Flask app
- **`railway.json`** - Railway deployment configuration
- **`runtime.txt`** - Specifies Python 3.11.0

### Static Frontend (GitHub Pages)
- **`docs/index.html`** - Home page (static version)
- **`docs/generate.html`** - Generate questions page
- **`docs/quiz.html`** - Quiz mode page
- **`docs/practice.html`** - Practice mode page
- **`docs/list.html`** - Question library page
- **`docs/css/style.css`** - Copied from `static/css/style.css`
- **`docs/js/config.js`** - API configuration (Railway URL)

### Documentation
- **`DEPLOYMENT.md`** - Comprehensive deployment guide
- **`QUICK_START.md`** - 10-minute quick start guide
- **`.github/DEPLOYMENT_CHECKLIST.md`** - Deployment checklist

## Modified Files

### `requirements.txt`
**Added:**
- `flask-cors>=4.0.0` - Enable CORS for API access from GitHub Pages
- `gunicorn>=21.2.0` - Production WSGI server for Railway

### `app.py`
**Added:**
```python
from flask_cors import CORS
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'grade3-quiz-secret-key')
CORS(app)
```

**Purpose:**
- Enable CORS to allow frontend on GitHub Pages to call backend on Railway
- Support environment variables for production secrets

### `README.md`
**Added:**
- Deployment section with links to guides
- Information about free hosting options

## Architecture Changes

### Before
```
Single Flask App
├── Templates (Jinja2)
├── Static files
├── Database (SQLite)
└── Run locally with `python app.py`
```

### After
```
Split Architecture

Backend (Railway)                    Frontend (GitHub Pages)
├── Flask API                        ├── Static HTML files
├── Database (SQLite)                ├── CSS files
├── Question Generator               ├── JavaScript
└── REST endpoints                   └── Calls backend API
```

## How It Works

1. **User visits GitHub Pages URL**
   - `https://username.github.io/grade3-question-generator/`
   - Loads static HTML/CSS/JS files

2. **JavaScript makes API calls**
   - Configured in `docs/js/config.js`
   - Calls Railway backend: `https://xyz.up.railway.app/api/...`

3. **Flask backend responds**
   - CORS headers allow cross-origin requests
   - Processes requests, queries database
   - Returns JSON responses

4. **Frontend displays results**
   - JavaScript updates the page
   - User sees questions, scores, etc.

## API Endpoints Used

All endpoints are called from the frontend:

- `POST /api/generate` - Generate questions
- `GET /api/questions` - List questions
- `POST /api/practice/start` - Start practice session
- `POST /api/quiz/question` - Get quiz question
- `POST /api/quiz/check` - Check quiz answer

## Environment Variables

### Railway (Optional)
- `SECRET_KEY` - Flask session secret
- `LLAMA_URL` - LLM endpoint URL

### GitHub Pages
- No environment variables needed
- API URL configured in `docs/js/config.js`

## Cost Breakdown

### FREE Setup
- **Railway:** 500 hours/month free (≈16 hours/day)
- **GitHub Pages:** Unlimited free for public repos
- **Total:** $0/month for typical usage

### If Needed
- Railway Pro: $5/month (500 hours + $0.000231/GB-hour)
- Persistent storage (PostgreSQL): Available on Railway

## Migration Path

### From Local to Deployed

1. **Continue developing locally:**
   ```bash
   python app.py  # Run Flask locally on port 5001
   ```

2. **Test with local backend:**
   - Set `API_BASE_URL = 'http://localhost:5001'` in `docs/js/config.js`
   - Open `docs/index.html` in browser

3. **Deploy to production:**
   - Deploy to Railway
   - Update `API_BASE_URL` to Railway URL
   - Push to GitHub (auto-deploys to GitHub Pages)

### Database Consideration

**Development:** SQLite (file-based, simple)

**Production Options:**
1. **SQLite on Railway** (current setup)
   - ✅ No changes needed
   - ⚠️ Data lost on restart (free tier limitation)
   - ✅ Good for demo/testing

2. **PostgreSQL on Railway** (recommended for production)
   - ✅ Persistent data
   - ✅ Included in Railway free tier
   - ⚠️ Requires code changes in `database.py`

## Security Considerations

1. **CORS:** Currently allows all origins
   - Production: Restrict to your GitHub Pages domain only

2. **API Rate Limiting:** Not implemented
   - Consider adding to prevent abuse

3. **Input Validation:** Already implemented in Flask

4. **Secrets:** Never commit to Git
   - Use Railway environment variables

## Rollback Plan

If deployment fails, you can:

1. **Backend:**
   - Railway keeps previous deployments
   - Can roll back via Railway dashboard

2. **Frontend:**
   - Revert commit in Git
   - Push to GitHub

3. **Local Development:**
   - Original `templates/` folder still works
   - Run `python app.py` as before

## Future Enhancements

Possible improvements:

1. **Custom Domain:**
   - Add custom domain to GitHub Pages
   - Update CORS to allow only your domain

2. **Persistent Database:**
   - Add PostgreSQL to Railway
   - Modify `database.py` to support PostgreSQL

3. **Analytics:**
   - Add Google Analytics to track usage
   - Monitor popular features

4. **PWA (Progressive Web App):**
   - Add service worker
   - Enable offline mode
   - Install as mobile app

5. **Authentication:**
   - Add user accounts
   - Track individual progress
   - Teacher dashboard

## Support

- **Railway Issues:** https://railway.app/help
- **GitHub Pages Issues:** https://docs.github.com/pages
- **Project Issues:** Open issue on GitHub repository

## Summary

✅ **What was added:**
- Railway deployment configuration
- Static frontend for GitHub Pages
- CORS support for cross-origin API calls
- Comprehensive documentation

✅ **What stayed the same:**
- All original functionality
- Local development workflow
- CLI interface
- Database schema
- Question generation logic

✅ **What you get:**
- Free hosting for backend and frontend
- Public URL anyone can access
- Auto-deployment from GitHub
- No servers to maintain
