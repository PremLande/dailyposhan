# PostgreSQL Setup Guide for Daily Poshan

## Prerequisites

Before setting up the database, make sure you have PostgreSQL installed and running.

### Install PostgreSQL

#### Windows
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer
3. Set password for postgres user (remember this password)
4. Keep default port (5432)

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### macOS
```bash
brew install postgresql
brew services start postgresql
```

### Create Database User (Optional but recommended)

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database user
CREATE USER dailyposhan_user WITH PASSWORD 'your_secure_password';

-- Create database
CREATE DATABASE dailyposhan_db OWNER dailyposhan_user;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE dailyposhan_db TO dailyposhan_user;
```

## Configuration

### 1. Update Environment Variables

Edit `backend-django/.env.local`:

```env
# Database Configuration
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=dailyposhan_db
DATABASE_USER=postgres  # or dailyposhan_user if you created one
DATABASE_PASSWORD=your_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Alternative: Use DATABASE_URL
# DATABASE_URL=postgresql://postgres:your_password_here@localhost:5432/dailyposhan_db
```

### 2. Install Dependencies

```bash
cd backend-django
pip install -r requirements.txt
```

### 3. Initialize Database

Choose one of the following methods:

#### Method A: Using Python Script (Recommended)
```bash
cd database
python init_db.py
```

#### Method B: Using Django Management Command
```bash
cd backend-django
python manage.py init_db --sample-data
```

#### Method C: Manual Setup
```bash
# Create database
createdb -U postgres dailyposhan_db

# Run schema
psql -U postgres -d dailyposhan_db -f database/schema.sql

# Run Django migrations
cd backend-django
python manage.py migrate
```

### 4. Test Connection

```bash
cd backend-django
python manage.py dbshell
```

You should be able to connect to PostgreSQL. Type `\q` to exit.

### 5. Run the Server

```bash
python manage.py runserver
```

## Troubleshooting

### Connection Issues

1. **PostgreSQL not running:**
   ```bash
   # Windows
   net start postgresql-x64-14

   # Linux
   sudo systemctl status postgresql

   # macOS
   brew services list
   ```

2. **Authentication failed:**
   - Check password in `.env.local`
   - Make sure user exists: `psql -U postgres -c "SELECT * FROM pg_user;"`

3. **Database doesn't exist:**
   ```sql
   psql -U postgres -c "CREATE DATABASE dailyposhan_db;"
   ```

### Permission Issues

```sql
-- Grant all permissions
GRANT ALL PRIVILEGES ON DATABASE dailyposhan_db TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
```

### Port Issues

If port 5432 is busy, check what's using it:
```bash
# Windows
netstat -ano | findstr :5432

# Linux/macOS
lsof -i :5432
```

## Production Deployment

For production, use environment variables or DATABASE_URL:

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

Or individual settings:
```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=prod_db
DATABASE_USER=prod_user
DATABASE_PASSWORD=secure_password
DATABASE_HOST=your-db-host.com
DATABASE_PORT=5432
DATABASE_SSL_MODE=require
```

## Backup and Restore

### Backup
```bash
pg_dump -U postgres -h localhost dailyposhan_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore
```bash
psql -U postgres -d dailyposhan_db < backup_file.sql
```

## Next Steps

Once PostgreSQL is set up:

1. Run the Django server: `python manage.py runserver`
2. Test the API endpoints
3. Check that data is being stored in PostgreSQL
4. Monitor database performance and connections

The application is now configured to use PostgreSQL instead of SQLite!