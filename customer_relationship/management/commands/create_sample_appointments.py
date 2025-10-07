from django.core.management.base import BaseCommand
from customer_relationship.models import Customer, AppointmentType, Appointment
from datetime import datetime, timedelta
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Create sample appointment types and appointments for testing the API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--appointment-types',
            type=int,
            default=5,
            help='Number of appointment types to create (default: 5)',
        )
        parser.add_argument(
            '--appointments',
            type=int,
            default=10,
            help='Number of appointments to create (default: 10)',
        )

    def handle(self, *args, **options):
        appointment_types_count = options['appointment_types']
        appointments_count = options['appointments']
        
        # Sample appointment types
        sample_appointment_types = [
            {"description": "Haircut"},
            {"description": "Hair Coloring"},
            {"description": "Manicure"},
            {"description": "Pedicure"},
            {"description": "Facial Treatment"},
            {"description": "Eyebrow Shaping"},
            {"description": "Hair Washing"},
            {"description": "Blowdry"},
            {"description": "Hair Treatment"},
            {"description": "Makeup Session"},
        ]
        
        # Create appointment types
        created_types_count = 0
        appointment_types = []
        
        for i in range(appointment_types_count):
            type_data = sample_appointment_types[i % len(sample_appointment_types)].copy()
            
            # Make description unique if creating multiple copies
            if i >= len(sample_appointment_types):
                type_data['description'] = f"{type_data['description']} {i + 1}"
            
            try:
                appointment_type, created = AppointmentType.objects.get_or_create(
                    description=type_data['description']
                )
                if created:
                    created_types_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created appointment type: {appointment_type.description}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Appointment type already exists: {appointment_type.description}'
                        )
                    )
                appointment_types.append(appointment_type)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating appointment type {type_data["description"]}: {str(e)}'
                    )
                )
        
        # Get all customers for creating appointments
        customers = list(Customer.objects.all())
        if not customers:
            self.stdout.write(
                self.style.ERROR(
                    'No customers found! Please create customers first using: '
                    'python manage.py create_sample_customers'
                )
            )
            return
        
        # Create appointments
        created_appointments_count = 0
        now = timezone.now()
        
        # Sample appointment data patterns
        appointment_patterns = [
            {"duration_minutes": 30, "status": "scheduled", "notes": "Regular appointment"},
            {"duration_minutes": 60, "status": "confirmed", "notes": "Customer requested a specific stylist"},
            {"duration_minutes": 45, "status": "scheduled", "notes": "First time customer"},
            {"duration_minutes": 90, "status": "confirmed", "notes": "Full service appointment"},
            {"duration_minutes": 30, "status": "cancelled", "notes": "Customer requested rescheduling", "cancellation_reason": "Schedule conflict"},
            {"duration_minutes": 120, "status": "confirmed", "notes": "Special occasion preparation"},
            {"duration_minutes": 45, "status": "scheduled", "notes": "Regular maintenance"},
            {"duration_minutes": 60, "status": "confirmed", "notes": "Color touch-up"},
        ]
        
        for i in range(appointments_count):
            pattern = appointment_patterns[i % len(appointment_patterns)]
            
            # Generate random start time (from yesterday to 30 days in the future)
            days_offset = random.randint(-1, 30)
            hour = random.randint(9, 17)  # Business hours
            minute = random.choice([0, 15, 30, 45])  # 15-minute intervals
            
            start_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0) + timedelta(days=days_offset)
            end_time = start_time + timedelta(minutes=pattern["duration_minutes"])
            
            appointment_data = {
                "customer": random.choice(customers),
                "appointment_type": random.choice(appointment_types),
                "start_time": start_time,
                "end_time": end_time,
                "status": pattern["status"],
                "notes": pattern["notes"],
            }
            
            # Add cancellation reason if cancelled
            if pattern["status"] == "cancelled" and "cancellation_reason" in pattern:
                appointment_data["cancellation_reason"] = pattern["cancellation_reason"]
            
            try:
                appointment = Appointment.objects.create(**appointment_data)
                created_appointments_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created appointment: {appointment.customer.full_name} - '
                        f'{appointment.appointment_type.description} on '
                        f'{appointment.start_time.strftime("%Y-%m-%d %H:%M")} '
                        f'({appointment.status})'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating appointment: {str(e)}'
                    )
                )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created:'
                f'\n- {created_types_count} appointment types'
                f'\n- {created_appointments_count} appointments'
            )
        )
        
        if created_appointments_count > 0 or created_types_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\nYou can now test the API endpoints:'
                    f'\n- Visit http://127.0.0.1:8000/api/appointment-types/ to see all appointment types'
                    f'\n- Visit http://127.0.0.1:8000/api/appointments/ to see all appointments'
                    f'\n- Visit http://127.0.0.1:8000/api/appointments/today/ to see today\'s appointments'
                    f'\n- Visit http://127.0.0.1:8000/api/appointments/upcoming/ to see upcoming appointments'
                    f'\n- Visit http://127.0.0.1:8000/admin/ to manage appointments in Django admin'
                )
            )