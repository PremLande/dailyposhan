from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Initialize PostgreSQL database with schema and sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sample-data',
            action='store_true',
            help='Add sample data for testing',
        )

    def handle(self, *args, **options):
        self.stdout.write('Initializing Daily Poshan PostgreSQL database...')

        # Get schema file path
        schema_path = Path(__file__).parent.parent.parent.parent / 'database' / 'schema.sql'

        if not schema_path.exists():
            self.stderr.write(f'Schema file not found: {schema_path}')
            return

        try:
            # Read schema
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            # Execute schema (split by semicolon for PostgreSQL)
            with connection.cursor() as cursor:
                statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
                for statement in statements:
                    if statement:
                        try:
                            cursor.execute(statement)
                        except Exception as stmt_error:
                            self.stdout.write(
                                self.style.WARNING(f'Warning executing statement: {stmt_error}')
                            )

            self.stdout.write(
                self.style.SUCCESS('✓ Database schema created successfully')
            )

            # Verify tables were created
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables = cursor.fetchall()

            table_names = [table[0] for table in tables]
            expected_tables = ['users', 'products', 'orders', 'order_items', 'addresses', 'payments']

            for table in expected_tables:
                if table in table_names:
                    self.stdout.write(f'✓ Table "{table}" created')
                else:
                    self.stdout.write(
                        self.style.WARNING(f'✗ Table "{table}" not found')
                    )

            # Add sample data if requested
            if options['sample_data']:
                self.add_sample_data()

        except Exception as e:
            self.stderr.write(f'Error initializing database: {e}')

    def add_sample_data(self):
        """Add sample data for testing"""
        try:
            from apps.products.models import Product
            from apps.payments.models import Address

            # Create sample products if not exist
            if Product.objects.count() == 0:
                products_data = [
                    {
                        'name': 'Muscle Fuel Jar',
                        'price': 249,
                        'calories': 420,
                        'protein': '34g',
                        'description': 'High protein meal replacement for muscle building',
                        'stock': 100
                    },
                    {
                        'name': 'Glow & Flow Jar',
                        'price': 229,
                        'calories': 310,
                        'protein': '14g',
                        'description': 'Nutrient-rich meal for healthy skin and digestion',
                        'stock': 100
                    },
                    {
                        'name': 'Chatori Jar',
                        'price': 199,
                        'calories': 260,
                        'protein': '12g',
                        'description': 'Light and nutritious meal option',
                        'stock': 100
                    }
                ]

                for product_data in products_data:
                    Product.objects.create(**product_data)

                self.stdout.write(f'✓ {len(products_data)} sample products created')

            # Create sample addresses
            if Address.objects.count() == 0:
                addresses_data = [
                    {
                        'customer_name': 'John Doe',
                        'phone': '+91-9876543210',
                        'full_address': '123 Main Street, Mumbai, Maharashtra',
                        'pincode': '400001',
                        'is_default': True
                    },
                    {
                        'customer_name': 'Jane Smith',
                        'phone': '+91-9876543211',
                        'full_address': '456 Park Avenue, Delhi, Delhi',
                        'pincode': '110001',
                        'is_default': False
                    }
                ]

                for address_data in addresses_data:
                    Address.objects.create(**address_data)

                self.stdout.write(f'✓ {len(addresses_data)} sample addresses created')

            self.stdout.write(
                self.style.SUCCESS('✓ Sample data added successfully')
            )

        except Exception as e:
            self.stderr.write(f'Error adding sample data: {e}')