# Database Setup - PostgreSQL

This directory contains database-related files for the Daily Poshan project using PostgreSQL.

## Files

- `schema.sql` - Complete PostgreSQL database schema with tables, indexes, triggers, and initial data
- `init_db.py` - Python script to initialize the PostgreSQL database
- `README.md` - This file

## Prerequisites

Before running the database setup, make sure you have:

1. **PostgreSQL installed and running** on your system
2. **Database user and password** configured
3. **Environment variables** set in `.env.local` file

## Environment Configuration

Update your `backend-django/.env.local` file with PostgreSQL credentials:

```env
# Database Configuration
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=dailyposhan_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Alternative: Use DATABASE_URL (uncomment and set if using connection URL)
# DATABASE_URL=postgresql://postgres:your_password_here@localhost:5432/dailyposhan_db

# Database SSL and Connection Settings
DATABASE_SSL_MODE=require
DATABASE_CONN_MAX_AGE=600
DATABASE_ATOMIC_REQUESTS=False
```

## Database Schema

The database uses PostgreSQL and includes the following tables:

### Core Tables

1. **users** - User accounts (admin/customer)
2. **products** - Product catalog
3. **orders** - Order records
4. **order_items** - Individual items in orders
5. **addresses** - Customer delivery addresses
6. **payments** - Payment records

### Features

- SERIAL PRIMARY KEY for auto-incrementing IDs
- Foreign key constraints with CASCADE/RESTRICT options
- Data validation with CHECK constraints
- Automatic timestamps with timezone
- Triggers for timestamp updates
- Indexes for performance optimization

## Setup Instructions

### Option 1: Using Python Script (Recommended)

```bash
cd database
python init_db.py
```

This script will:
- Create the database if it doesn't exist
- Run the schema.sql file
- Add initial product data
- Optionally add sample data

### Option 2: Manual Setup

1. **Create database:**
   ```sql
   CREATE DATABASE dailyposhan_db;
   ```

2. **Run schema:**
   ```bash
   psql -U postgres -d dailyposhan_db -f schema.sql
   ```

3. **Run Django migrations:**
   ```bash
   cd backend-django
   python manage.py migrate
   ```

### Option 3: Using Django Management Command

```bash
cd backend-django
python manage.py init_db --sample-data
```

## Initial Data

The schema includes:

- 3 sample products (Muscle Fuel Jar, Glow & Flow Jar, Chatori Jar)
- Sample addresses and orders (when using --sample-data)

## Database Views

- `order_summary` - Orders with item counts and totals
- `product_sales` - Product sales statistics
- `order_stats` - Overall order statistics

## PostgreSQL-Specific Features

- **Triggers**: Automatic timestamp updates using PostgreSQL functions
- **Data Types**: Proper VARCHAR lengths, TEXT for large content
- **Constraints**: CHECK constraints for data validation
- **Timezones**: TIMESTAMP WITH TIME ZONE for proper time handling

## Troubleshooting

### Connection Issues
- Make sure PostgreSQL is running: `sudo systemctl status postgresql`
- Check credentials in `.env.local`
- Verify user has database creation privileges

### Permission Issues
```sql
-- Grant permissions if needed
GRANT ALL PRIVILEGES ON DATABASE dailyposhan_db TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
```

### Migration Issues
If you encounter migration issues, you can:
1. Drop and recreate the database
2. Run `python manage.py migrate --fake-initial`
3. Check Django migration files

## Backup and Restore

### Backup
```bash
pg_dump -U postgres -h localhost dailyposhan_db > backup.sql
```

### Restore
```bash
psql -U postgres -h localhost dailyposhan_db < backup.sql
```

## Production Deployment

For production, consider:

1. **Connection pooling** with PgBouncer
2. **SSL connections** for security
3. **Regular backups** and monitoring
4. **Database user** with limited privileges
5. **Environment variables** for all credentials

## Development vs Production

- **Development**: Use local PostgreSQL with full access
- **Production**: Use managed PostgreSQL (AWS RDS, Google Cloud SQL, etc.) with DATABASE_URL