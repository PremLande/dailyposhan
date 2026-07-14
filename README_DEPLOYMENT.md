# Free deployment guide

## Backend on Render
1. Create a Render account.
2. Connect this GitHub repository.
3. Choose "New > Web Service".
4. Select the repo and set the root directory to `backend-django`.
5. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python manage.py migrate && gunicorn dailyposhan_backend.wsgi:application --bind 0.0.0.0:$PORT`
6. Add environment variables:
   - `SECRET_KEY`: any secure value
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*`
   - `CORS_ALLOWED_ORIGINS`: `https://<your-vercel-app>.vercel.app,http://localhost:5173`
7. Create a PostgreSQL database in Render and link it as `DATABASE_URL`.

## Frontend on Vercel
1. Create a Vercel account.
2. Import the `frontend-react` folder as a project.
3. Set the build command to `npm run build`.
4. Set the output directory to `dist`.
5. Add the environment variable:
   - `VITE_API_BASE_URL=/api`

## Notes
- The Vercel config rewrites `/api/*` to your Render backend.
- Replace the placeholder backend URL in `frontend-react/vercel.json` with your actual Render URL after deployment.
