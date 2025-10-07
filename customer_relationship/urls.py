from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, AppointmentTypeViewSet, AppointmentViewSet

# Create a router and register the ViewSets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'appointment-types', AppointmentTypeViewSet, basename='appointment-type')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

app_name = 'customer_relationship'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
]

# Available API endpoints:

# CUSTOMERS:
# GET /api/customers/ - List all customers (with pagination, filtering, search)
# POST /api/customers/ - Create a new customer
# GET /api/customers/{uuid}/ - Retrieve a specific customer
# PUT /api/customers/{uuid}/ - Update a specific customer (full update)
# PATCH /api/customers/{uuid}/ - Partial update a specific customer
# DELETE /api/customers/{uuid}/ - Delete a specific customer
# GET /api/customers/active/ - List only active customers
# POST /api/customers/{uuid}/deactivate/ - Deactivate a customer
# POST /api/customers/{uuid}/activate/ - Activate a customer
# GET /api/customers/search_advanced/ - Advanced search with multiple criteria

# APPOINTMENT TYPES:
# GET /api/appointment-types/ - List all appointment types (with pagination, filtering, search)
# POST /api/appointment-types/ - Create a new appointment type
# GET /api/appointment-types/{uuid}/ - Retrieve a specific appointment type
# PUT /api/appointment-types/{uuid}/ - Update a specific appointment type (full update)
# PATCH /api/appointment-types/{uuid}/ - Partial update a specific appointment type
# DELETE /api/appointment-types/{uuid}/ - Delete a specific appointment type

# APPOINTMENTS:
# GET /api/appointments/ - List all appointments (with pagination, filtering, search)
# POST /api/appointments/ - Create a new appointment
# GET /api/appointments/{uuid}/ - Retrieve a specific appointment
# PUT /api/appointments/{uuid}/ - Update a specific appointment (full update)
# PATCH /api/appointments/{uuid}/ - Partial update a specific appointment
# DELETE /api/appointments/{uuid}/ - Delete a specific appointment
# GET /api/appointments/today/ - List appointments for today
# GET /api/appointments/upcoming/ - List upcoming appointments
# POST /api/appointments/{uuid}/confirm/ - Confirm an appointment
# POST /api/appointments/{uuid}/cancel/ - Cancel an appointment
# GET /api/appointments/by_customer/ - Get appointments for a specific customer

# Query parameters for filtering:
# Customers: ?is_active=true/false, ?gender=male/female/other, ?address_country=USA, etc.
# Appointments: ?status=scheduled/confirmed/cancelled, ?appointment_type={uuid}, ?customer={uuid}
# ?search=term (searches in relevant fields)
# ?ordering=created_at,-updated_at,start_time,-end_time (for appointments)

# Advanced search query parameters:
# Customer search: ?name=John, ?location=New York, ?tags=VIP,Diabetic, ?preferences=whatsapp_news
# Appointment search: ?customer_uuid={uuid} (for by_customer endpoint)