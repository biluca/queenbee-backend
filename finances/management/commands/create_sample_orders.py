from django.core.management.base import BaseCommand
from finances.models import OrderType, PaymentType, OrderItem, Order, OrderItemLine
from customer_relationship.models import Customer, Appointment
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create sample order types, payment types, order items and orders for testing the API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--order-items',
            type=int,
            default=15,
            help='Number of order items to create (default: 15)',
        )
        parser.add_argument(
            '--orders',
            type=int,
            default=20,
            help='Number of orders to create (default: 20)',
        )

    def handle(self, *args, **options):
        order_items_count = options['order_items']
        orders_count = options['orders']
        
        self.stdout.write(self.style.SUCCESS('Creating sample financial data...'))
        
        # Create OrderTypes
        order_types_created = self.create_order_types()
        
        # Create PaymentTypes
        payment_types_created = self.create_payment_types()
        
        # Create OrderItems
        order_items_created = self.create_order_items(order_items_count)
        
        # Create Orders
        orders_created = self.create_orders(orders_count)
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created:'
                f'\n- {order_types_created} order types'
                f'\n- {payment_types_created} payment types'
                f'\n- {order_items_created} order items'
                f'\n- {orders_created} orders'
            )
        )
        
        if orders_created > 0 or order_items_created > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\nYou can now test the API endpoints:'
                    f'\n- Visit http://127.0.0.1:8000/finances/api/orders/ to see all orders'
                    f'\n- Visit http://127.0.0.1:8000/finances/api/order-items/ to see all order items'
                    f'\n- Visit http://127.0.0.1:8000/finances/api/orders/statistics/ to see financial statistics'
                    f'\n- Visit http://127.0.0.1:8000/finances/api/orders/income/ to see income orders'
                    f'\n- Visit http://127.0.0.1:8000/finances/api/orders/expense/ to see expense orders'
                    f'\n- Visit http://127.0.0.1:8000/admin/finances/ to manage financial data in Django admin'
                )
            )

    def create_order_types(self):
        """Create sample order types"""
        order_types_data = [
            {"type": "Income"},
            {"type": "Expense"},
        ]
        
        created_count = 0
        for type_data in order_types_data:
            try:
                order_type, created = OrderType.objects.get_or_create(**type_data)
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created order type: {order_type.type}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Order type already exists: {order_type.type}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating order type {type_data["type"]}: {str(e)}')
                )
        
        return created_count

    def create_payment_types(self):
        """Create sample payment types"""
        payment_types_data = [
            {"type": "Cash"},
            {"type": "Credit Card"},
            {"type": "Debit Card"},
            {"type": "Exchange"},
            {"type": "Bank Slip"},
            {"type": "Pix"},
        ]
        
        created_count = 0
        for type_data in payment_types_data:
            try:
                payment_type, created = PaymentType.objects.get_or_create(**type_data)
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created payment type: {payment_type.type}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Payment type already exists: {payment_type.type}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating payment type {type_data["type"]}: {str(e)}')
                )
        
        return created_count

    def create_order_items(self, count):
        """Create sample order items"""
        sample_order_items = [
            # Beauty Products
            {"description": "Professional Shampoo", "inventory_quantity": 25, "unit_price": Decimal("29.99")},
            {"description": "Hair Conditioner", "inventory_quantity": 20, "unit_price": Decimal("24.99")},
            {"description": "Hair Styling Gel", "inventory_quantity": 15, "unit_price": Decimal("18.50")},
            {"description": "Hair Serum", "inventory_quantity": 12, "unit_price": Decimal("35.00")},
            {"description": "Face Moisturizer", "inventory_quantity": 30, "unit_price": Decimal("45.00")},
            
            # Nail Care
            {"description": "Nail Polish - Red", "inventory_quantity": 8, "unit_price": Decimal("12.99")},
            {"description": "Nail Polish - Pink", "inventory_quantity": 10, "unit_price": Decimal("12.99")},
            {"description": "Nail Base Coat", "inventory_quantity": 15, "unit_price": Decimal("15.99")},
            {"description": "Nail Top Coat", "inventory_quantity": 15, "unit_price": Decimal("15.99")},
            {"description": "Cuticle Oil", "inventory_quantity": 20, "unit_price": Decimal("8.99")},
            
            # Accessories
            {"description": "Hair Brush - Professional", "inventory_quantity": 5, "unit_price": Decimal("55.00")},
            {"description": "Hair Clips Set", "inventory_quantity": 25, "unit_price": Decimal("12.99")},
            {"description": "Makeup Sponges Pack", "inventory_quantity": 40, "unit_price": Decimal("9.99")},
            
            # Services (non-inventory items)
            {"description": "Haircut Service", "inventory_quantity": 0, "unit_price": Decimal("45.00")},
            {"description": "Hair Coloring Service", "inventory_quantity": 0, "unit_price": Decimal("85.00")},
            {"description": "Manicure Service", "inventory_quantity": 0, "unit_price": Decimal("25.00")},
            {"description": "Pedicure Service", "inventory_quantity": 0, "unit_price": Decimal("35.00")},
            {"description": "Facial Treatment Service", "inventory_quantity": 0, "unit_price": Decimal("60.00")},
            {"description": "Eyebrow Shaping Service", "inventory_quantity": 0, "unit_price": Decimal("20.00")},
            {"description": "Hair Treatment Service", "inventory_quantity": 0, "unit_price": Decimal("40.00")},
            
            # Equipment/Expenses
            {"description": "Hair Dryer - Professional", "inventory_quantity": 2, "unit_price": Decimal("150.00")},
            {"description": "Salon Chair", "inventory_quantity": 1, "unit_price": Decimal("350.00")},
            {"description": "Mirror - Salon Grade", "inventory_quantity": 3, "unit_price": Decimal("120.00")},
            {"description": "Sterilization Equipment", "inventory_quantity": 1, "unit_price": Decimal("200.00")},
        ]
        
        created_count = 0
        for i in range(count):
            item_data = sample_order_items[i % len(sample_order_items)].copy()
            
            # Make description unique if creating multiple copies
            if i >= len(sample_order_items):
                item_data['description'] = f"{item_data['description']} - {i + 1}"
            
            try:
                order_item, created = OrderItem.objects.get_or_create(
                    description=item_data['description'],
                    defaults={
                        'inventory_quantity': item_data['inventory_quantity'],
                        'unit_price': item_data['unit_price']
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created order item: {order_item.description} - ${order_item.unit_price}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Order item already exists: {order_item.description}'
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating order item {item_data["description"]}: {str(e)}'
                    )
                )
        
        return created_count

    def create_orders(self, count):
        """Create sample orders with order items"""
        # Get required data
        customers = list(Customer.objects.all())
        if not customers:
            self.stdout.write(
                self.style.ERROR(
                    'No customers found! Please create customers first using: '
                    'python manage.py create_sample_customers'
                )
            )
            return 0
        
        order_types = list(OrderType.objects.all())
        payment_types = list(PaymentType.objects.all())
        order_items = list(OrderItem.objects.all())
        appointments = list(Appointment.objects.all())
        
        if not order_types or not payment_types or not order_items:
            self.stdout.write(
                self.style.ERROR(
                    'Missing required data! Please ensure order types, payment types, '
                    'and order items are created first.'
                )
            )
            return 0
        
        created_count = 0
        now = timezone.now()
        
        # Order patterns for different scenarios
        order_patterns = [
            # Income orders (services + products)
            {
                "order_type": "Income",
                "items": [
                    {"type": "service", "quantity": 1},
                    {"type": "product", "quantity": random.randint(1, 2)}
                ]
            },
            # Income orders (services only)
            {
                "order_type": "Income",
                "items": [
                    {"type": "service", "quantity": 1}
                ]
            },
            # Income orders (products only)
            {
                "order_type": "Income",
                "items": [
                    {"type": "product", "quantity": random.randint(1, 3)}
                ]
            },
            # Expense orders (equipment/supplies)
            {
                "order_type": "Expense",
                "items": [
                    {"type": "equipment", "quantity": 1}
                ]
            },
        ]
        
        # Separate order items by type
        service_items = [item for item in order_items if item.inventory_quantity == 0]
        product_items = [item for item in order_items if item.inventory_quantity > 0 and item.unit_price < 100]
        equipment_items = [item for item in order_items if item.inventory_quantity > 0 and item.unit_price >= 100]
        
        for i in range(count):
            # Choose pattern (80% income, 20% expense)
            if random.random() < 0.8:
                pattern = random.choice([p for p in order_patterns if p["order_type"] == "Income"])
            else:
                pattern = random.choice([p for p in order_patterns if p["order_type"] == "Expense"])
            
            # Generate random order date (from 30 days ago to today)
            days_offset = random.randint(-30, 0)
            order_date = now + timedelta(days=days_offset)
            
            try:
                # Create the order
                order_data = {
                    "customer": random.choice(customers),
                    "order_type": next(ot for ot in order_types if ot.type == pattern["order_type"]),
                    "payment_type": random.choice(payment_types),
                    "total": Decimal("0.00"),  # Will be calculated
                }
                
                # Optionally link to an appointment (30% chance for income orders)
                if pattern["order_type"] == "Income" and appointments and random.random() < 0.3:
                    order_data["appointment"] = random.choice(appointments)
                
                order = Order.objects.create(**order_data)
                
                # Create order items
                total_amount = Decimal("0.00")
                
                for item_pattern in pattern["items"]:
                    item_type = item_pattern["type"]
                    quantity = item_pattern["quantity"]
                    
                    # Select appropriate items based on type
                    if item_type == "service" and service_items:
                        available_items = service_items
                    elif item_type == "product" and product_items:
                        available_items = product_items
                    elif item_type == "equipment" and equipment_items:
                        available_items = equipment_items
                    else:
                        available_items = order_items  # Fallback
                    
                    selected_item = random.choice(available_items)
                    
                    # Create order item line
                    order_item_line = OrderItemLine.objects.create(
                        order=order,
                        order_item=selected_item,
                        quantity=quantity,
                        unit_price=selected_item.unit_price
                    )
                    
                    total_amount += order_item_line.total_price
                
                # Update order total
                order.total = total_amount
                order.save()
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created order: {order.customer.full_name} - '
                        f'{order.order_type.type} - ${order.total} '
                        f'({order.payment_type.type})'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating order: {str(e)}')
                )
        
        return created_count