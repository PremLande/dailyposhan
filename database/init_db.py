#!/usr/bin/env python3
"""
Database Initialization Script for Daily Poshan - PostgreSQL
This script creates the database and populates it with initial data.
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('DATABASE_HOST', 'localhost'),
        'port': os.getenv('DATABASE_PORT', '5444'),
        'database': os.getenv('DATABASE_NAME', 'postgres'),
        'user': os.getenv('DATABASE_USER', 'postgres'),
        'password': os.getenv('DATABASE_PASSWORD', 'dailyposhan7030'),
    }

def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    config = get_db_config()

    # Connect to default postgres database to create our database
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database='postgres',
            user=config['user'],
            password=config['password']
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (config['database'],))
        if not cursor.fetchone():
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(config['database'])
            ))
            print(f"✓ Database '{config['database']}' created")
        else:
            print(f"✓ Database '{config['database']}' already exists")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error creating database: {e}")
        print("Make sure PostgreSQL is running and credentials are correct.")
        return False

def init_database():
    """Initialize the database with schema and initial data"""
    config = get_db_config()

    print(f"Initializing PostgreSQL database at: {config['host']}:{config['port']}/{config['database']}")

    # Get schema file path
    schema_path = Path(__file__).parent / "schema.sql"
    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}")
        return False

    try:
        # Read schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # Connect to database
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # Execute schema (split by semicolon and execute each statement)
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                except Exception as stmt_error:
                    print(f"Warning executing statement: {stmt_error}")
                    # Continue with other statements

        # Commit changes
        conn.commit()

        print("✓ Database schema created successfully")

        # Verify tables were created
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]

        expected_tables = ['users', 'products', 'orders', 'order_items', 'addresses', 'payments']
        for table in expected_tables:
            if table in table_names:
                print(f"✓ Table '{table}' created")
            else:
                print(f"✗ Table '{table}' not found")

        # Check initial data
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"✓ Products: {product_count}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error initializing database: {e}")
        print("Make sure PostgreSQL is running and database credentials are correct.")
        return False

def seed_sample_data():
    """Add sample data for testing"""
    config = get_db_config()

    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # Sample addresses
        sample_addresses = [
            ('John Doe', '+91-9876543210', '123 Main Street, Mumbai, Maharashtra', '400001', True),
            ('Jane Smith', '+91-9876543211', '456 Park Avenue, Delhi, Delhi', '110001', False),
            ('Raj Kumar', '+91-9876543212', '789 Gandhi Road, Bangalore, Karnataka', '560001', False),
        ]

        cursor.executemany("""
            INSERT INTO addresses (customer_name, phone, full_address, pincode, is_default)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, sample_addresses)

        # Sample orders
        sample_orders = [
            ('DP1640995200000', 'John Doe', '+91-9876543210', '123 Main Street, Mumbai, Maharashtra', 249, 'cod', 'Pending COD', 'Pending'),
            ('DP1641081600000', 'Jane Smith', '+91-9876543211', '456 Park Avenue, Delhi, Delhi', 478, 'online', 'Paid', 'Processing'),
        ]

        cursor.executemany("""
            INSERT INTO orders (id, customer_name, phone, address, total, payment_method, payment_status, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, sample_orders)

        # Sample order items
        sample_order_items = [
            ('DP1640995200000', 1, 'Muscle Fuel Jar', 1, 249),
            ('DP1641081600000', 2, 'Glow & Flow Jar', 1, 229),
            ('DP1641081600000', 3, 'Chatori Jar', 1, 199),
        ]

        cursor.executemany("""
            INSERT INTO order_items (order_id, product_id, product_name, quantity, price)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, sample_order_items)

        # Sample payments
        sample_payments = [
            ('PAYABC123456', 'DP1640995200000', 'cod', 'Pending', 249, None),
            ('PAYDEF789012', 'DP1641081600000', 'online', 'Completed', 478, 'TXN_123456789'),
        ]

        cursor.executemany("""
            INSERT INTO payments (id, order_id, method, status, amount, transaction_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, sample_payments)

        conn.commit()
        cursor.close()
        conn.close()

        print("✓ Sample data added successfully!")
        return True

    except Exception as e:
        print(f"Error adding sample data: {e}")
        return False

def main():
    """Main function"""
    print("Daily Poshan PostgreSQL Database Initialization")
    print("=" * 50)

    # Create database if needed
    if not create_database_if_not_exists():
        sys.exit(1)

    # Initialize database
    if not init_database():
        sys.exit(1)

    # Ask if user wants sample data
    response = input("\nAdd sample data for testing? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        if not seed_sample_data():
            sys.exit(1)

    print("\n🎉 PostgreSQL database setup complete!")
    print("You can now run the Django server.")

if __name__ == "__main__":
    main()