# Deployment Checklist

Use this checklist to ensure smooth deployment.

## Pre-Deployment

- [ ] All code changes committed
- [ ] Tests passing (if any)
- [ ] Dependencies up to date in `requirements.txt`
- [ ] `.gitignore` prevents committing secrets
- [ ] Database file (`questions.db`) not committed

## Railway Backend Deployment

- [ ] Railway account created
- [ ] GitHub repository connected to Railway
- [ ] Railway project created from GitHub repo
- [ ] Build completed successfully (check logs)
- [ ] Railway domain generated
- [ ] Backend URL copied (e.g., `https://xyz.up.railway.app`)
- [ ] Tested backend URL in browser
- [ ] Tested API endpoint: `/api/questions?subject=all&limit=10`

## Frontend Configuration

- [ ] `docs/js/config.js` updated with Railway URL
- [ ] No trailing slash in `API_BASE_URL`
- [ ] Changes committed to `docs/js/config.js`
- [ ] Pushed to GitHub master/main branch

## GitHub Pages Deployment

- [ ] Repository is public (required for free GitHub Pages)
- [ ] Changes merged to master/main branch
- [ ] GitHub Pages enabled in repository settings
- [ ] Source set to `master` (or `main`) branch
- [ ] Folder set to `/docs`
- [ ] Waited 2-3 minutes for deployment
- [ ] GitHub Actions build completed (check Actions tab)
- [ ] Frontend URL accessible (e.g., `https://username.github.io/grade3-question-generator/`)

## Testing

- [ ] Home page loads correctly
- [ ] All navigation links work
- [ ] Generate Questions page works
  - [ ] Can generate math questions
  - [ ] Can generate grammar questions
  - [ ] Questions are saved to backend
- [ ] List Questions page works
  - [ ] Shows saved questions
  - [ ] Filter by subject works
  - [ ] Statistics display correctly
- [ ] Practice Mode works
  - [ ] Can start practice session
  - [ ] Answer validation works
  - [ ] Score calculated correctly
- [ ] Quiz Mode works
  - [ ] Can start quiz
  - [ ] Both text and multiple-choice modes work
  - [ ] Streak counter updates
  - [ ] Wrong answer ends quiz
  - [ ] Results display correctly
- [ ] Responsive design works on mobile
- [ ] No console errors in browser (F12 → Console)

## Browser Testing

- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari
- [ ] Mobile browser

## Documentation

- [ ] README.md updated with deployment links
- [ ] DEPLOYMENT.md reviewed
- [ ] QUICK_START.md reviewed
- [ ] Links in documentation are correct

## Optional Enhancements

- [ ] Custom domain configured (GitHub Pages supports custom domains)
- [ ] Google Analytics added
- [ ] PostgreSQL database added to Railway (for persistence)
- [ ] Environment variables set in Railway
- [ ] Rate limiting added to API
- [ ] CORS restricted to specific domain only

## Post-Deployment

- [ ] Share URL with users
- [ ] Monitor Railway dashboard for errors
- [ ] Check Railway usage (stay within free tier)
- [ ] Bookmark Railway dashboard
- [ ] Bookmark GitHub Pages settings

## Monitoring (Weekly)

- [ ] Check Railway usage (hours remaining)
- [ ] Review error logs in Railway
- [ ] Test app functionality
- [ ] Check for security updates in dependencies

## When Making Updates

### Backend Updates
1. Make changes to Python files
2. Commit and push to GitHub
3. Railway auto-deploys
4. Check Railway logs for errors
5. Test API endpoints

### Frontend Updates
1. Make changes to `docs/` files
2. Commit and push to GitHub
3. GitHub Pages auto-deploys
4. Wait 1-2 minutes
5. Clear browser cache and test

---

## Need Help?

If something doesn't work:

1. Check this checklist - did you miss a step?
2. Review [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed instructions
3. Check Railway logs for backend errors
4. Check browser console (F12) for frontend errors
5. Verify `docs/js/config.js` has the correct Railway URL
6. Wait a few minutes and try again (deployments take time)

## Common Issues

**CORS errors:** Railway URL in `config.js` is wrong or has trailing slash

**404 on GitHub Pages:** Wait 2-3 minutes, check `/docs` folder exists on master

**Railway app crashes:** Check logs, verify `Procfile` and `requirements.txt`

**Questions don't persist:** Normal on Railway free tier (restarts clear SQLite) - add PostgreSQL for persistence
