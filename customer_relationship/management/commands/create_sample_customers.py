from django.core.management.base import BaseCommand
from customer_relationship.models import Customer
from datetime import date
import uuid


class Command(BaseCommand):
    help = 'Create sample customers for testing the API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of sample customers to create (default: 5)',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        sample_customers = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "nickname": "Big J",
                "email": "john.doe@example.com",
                "phone": "5551234567",
                "date_of_birth": date(1990, 1, 15),
                "gender": "male",
                "address_street": "123 Main Street",
                "address_number": "Apt 4B",
                "address_neighborhood": "Downtown",
                "address_city": "New York",
                "address_state": "NY",
                "address_zip_code": "10001",
                "address_country": "USA",
                "preferences": ["whatsapp_news", "email_news"],
                "tags": ["VIP"]
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "nickname": "Janie",
                "email": "jane.smith@example.com",
                "phone": "5559876543",
                "date_of_birth": date(1985, 5, 22),
                "gender": "female",
                "address_street": "456 Oak Avenue",
                "address_number": "Suite 12",
                "address_neighborhood": "Midtown",
                "address_city": "Los Angeles",
                "address_state": "CA",
                "address_zip_code": "90210",
                "address_country": "USA",
                "preferences": ["email_news"],
                "tags": ["Diabetic"]
            },
            {
                "first_name": "Carlos",
                "last_name": "Rodriguez",
                "nickname": "Charlie",
                "email": "carlos.rodriguez@example.com",
                "phone": "5555555555",
                "date_of_birth": date(1992, 8, 10),
                "gender": "male",
                "address_street": "789 Pine Road",
                "address_number": "Unit 5A",
                "address_neighborhood": "Southside",
                "address_city": "Miami",
                "address_state": "FL",
                "address_zip_code": "33101",
                "address_country": "USA",
                "preferences": ["whatsapp_news"],
                "tags": []
            },
            {
                "first_name": "Maria",
                "last_name": "Garcia",
                "nickname": "Mari",
                "email": "maria.garcia@example.com",
                "phone": "5551111111",
                "date_of_birth": date(1988, 12, 3),
                "gender": "female",
                "address_street": "321 Elm Street",
                "address_number": "Floor 2",
                "address_neighborhood": "Westside",
                "address_city": "Chicago",
                "address_state": "IL",
                "address_zip_code": "60601",
                "address_country": "USA",
                "preferences": ["whatsapp_news", "email_news"],
                "tags": ["VIP", "Diabetic"]
            },
            {
                "first_name": "David",
                "last_name": "Wilson",
                "nickname": "Dave",
                "email": "david.wilson@example.com",
                "phone": "5552222222",
                "date_of_birth": date(1995, 3, 18),
                "gender": "male",
                "address_street": "654 Maple Drive",
                "address_number": "Apt 8C",
                "address_neighborhood": "Northside",
                "address_city": "Seattle",
                "address_state": "WA",
                "address_zip_code": "98101",
                "address_country": "USA",
                "preferences": [],
                "tags": []
            }
        ]
        
        created_count = 0
        for i in range(count):
            customer_data = sample_customers[i % len(sample_customers)].copy()
            
            # Make email unique if creating multiple copies
            if i >= len(sample_customers):
                base_email = customer_data['email']
                name, domain = base_email.split('@')
                customer_data['email'] = f"{name}+{i}@{domain}"
            
            try:
                customer = Customer.objects.create(**customer_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created customer: {customer.full_name} ({customer.email})'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating customer {customer_data["email"]}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} out of {count} customers!'
            )
        )
        
        if created_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\nYou can now test the API endpoints:'
                    f'\n- Visit http://127.0.0.1:8000/api/customers/ to see all customers'
                    f'\n- Visit http://127.0.0.1:8000/admin/ to manage customers in Django admin'
                    f'\n- Run python customer_relationship/test_customer_api.py to test the API'
                )
            )