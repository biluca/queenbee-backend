from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from .models import Customer, AppointmentType, Appointment
from .serializers import (
    CustomerSerializer, CustomerCreateSerializer, CustomerUpdateSerializer,
    AppointmentTypeSerializer, AppointmentTypeCreateSerializer, AppointmentTypeUpdateSerializer,
    AppointmentSerializer, AppointmentCreateSerializer, AppointmentUpdateSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer CRUD operations
    
    Provides:
    - GET /api/customers/ - List all customers (with pagination, filtering, search)
    - POST /api/customers/ - Create a new customer
    - GET /api/customers/{uuid}/ - Retrieve a specific customer
    - PUT /api/customers/{uuid}/ - Update a specific customer (full update)
    - PATCH /api/customers/{uuid}/ - Partial update a specific customer
    - DELETE /api/customers/{uuid}/ - Delete a specific customer
    
    Additional endpoints:
    - GET /api/customers/active/ - List only active customers
    - POST /api/customers/{uuid}/deactivate/ - Deactivate a customer
    - POST /api/customers/{uuid}/activate/ - Activate a customer
    """
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'uuid'
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'gender', 'address_country', 'address_state', 'address_city']
    search_fields = ['first_name', 'last_name', 'nickname', 'email', 'phone']
    ordering_fields = ['created_at', 'updated_at', 'first_name', 'last_name', 'email']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return CustomerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CustomerUpdateSerializer
        return CustomerSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active customers"""
        active_customers = self.queryset.filter(is_active=True)
        page = self.paginate_queryset(active_customers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(active_customers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, uuid=None):
        """Deactivate a customer"""
        customer = self.get_object()
        customer.is_active = False
        customer.save()
        serializer = self.get_serializer(customer)
        return Response(
            {
                'message': 'Customer deactivated successfully',
                'customer': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def activate(self, request, uuid=None):
        """Activate a customer"""
        customer = self.get_object()
        customer.is_active = True
        customer.save()
        serializer = self.get_serializer(customer)
        return Response(
            {
                'message': 'Customer activated successfully',
                'customer': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def search_advanced(self, request):
        """Advanced search with multiple criteria"""
        queryset = self.queryset
        
        # Custom search parameters
        name = request.query_params.get('name', None)
        location = request.query_params.get('location', None)
        tags = request.query_params.get('tags', None)
        preferences = request.query_params.get('preferences', None)
        
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name) |
                Q(nickname__icontains=name)
            )
        
        if location:
            queryset = queryset.filter(
                Q(address_city__icontains=location) |
                Q(address_state__icontains=location) |
                Q(address_country__icontains=location)
            )
        
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                queryset = queryset.filter(tags__contains=[tag.strip()])
        
        if preferences:
            pref_list = preferences.split(',')
            for pref in pref_list:
                queryset = queryset.filter(preferences__contains=[pref.strip()])
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AppointmentTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AppointmentType CRUD operations
    
    Provides:
    - GET /api/appointment-types/ - List all appointment types (with pagination, filtering, search)
    - POST /api/appointment-types/ - Create a new appointment type
    - GET /api/appointment-types/{uuid}/ - Retrieve a specific appointment type
    - PUT /api/appointment-types/{uuid}/ - Update a specific appointment type (full update)
    - PATCH /api/appointment-types/{uuid}/ - Partial update a specific appointment type
    - DELETE /api/appointment-types/{uuid}/ - Delete a specific appointment type
    """
    
    queryset = AppointmentType.objects.all()
    serializer_class = AppointmentTypeSerializer
    lookup_field = 'uuid'
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description']
    ordering_fields = ['created_at', 'updated_at', 'description']
    ordering = ['description']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return AppointmentTypeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AppointmentTypeUpdateSerializer
        return AppointmentTypeSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment CRUD operations
    
    Provides:
    - GET /api/appointments/ - List all appointments (with pagination, filtering, search)
    - POST /api/appointments/ - Create a new appointment
    - GET /api/appointments/{uuid}/ - Retrieve a specific appointment
    - PUT /api/appointments/{uuid}/ - Update a specific appointment (full update)
    - PATCH /api/appointments/{uuid}/ - Partial update a specific appointment
    - DELETE /api/appointments/{uuid}/ - Delete a specific appointment
    
    Additional endpoints:
    - GET /api/appointments/today/ - List appointments for today
    - GET /api/appointments/upcoming/ - List upcoming appointments
    - POST /api/appointments/{uuid}/confirm/ - Confirm an appointment
    - POST /api/appointments/{uuid}/cancel/ - Cancel an appointment
    """
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    lookup_field = 'uuid'
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment_type', 'customer']
    search_fields = [
        'customer__first_name', 'customer__last_name', 'customer__email',
        'appointment_type__description', 'notes'
    ]
    ordering_fields = ['created_at', 'updated_at', 'start_time', 'end_time']
    ordering = ['-start_time']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return AppointmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AppointmentUpdateSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        """Optimize queryset with select_related"""
        return Appointment.objects.select_related('customer', 'appointment_type')
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get appointments for today"""
        today = timezone.now().date()
        today_appointments = self.get_queryset().filter(
            start_time__date=today
        )
        page = self.paginate_queryset(today_appointments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(today_appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments (from now onwards)"""
        now = timezone.now()
        upcoming_appointments = self.get_queryset().filter(
            start_time__gte=now,
            status__in=['scheduled', 'confirmed']
        )
        page = self.paginate_queryset(upcoming_appointments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(upcoming_appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, uuid=None):
        """Confirm an appointment"""
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(
            {
                'message': 'Appointment confirmed successfully',
                'appointment': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, uuid=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        appointment.status = 'cancelled'
        
        # Optional cancellation reason from request data
        cancellation_reason = request.data.get('cancellation_reason', '')
        if cancellation_reason:
            appointment.cancellation_reason = cancellation_reason
        
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(
            {
                'message': 'Appointment cancelled successfully',
                'appointment': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get appointments for a specific customer"""
        customer_uuid = request.query_params.get('customer_uuid', None)
        if not customer_uuid:
            return Response(
                {'error': 'customer_uuid parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        customer_appointments = self.get_queryset().filter(customer__uuid=customer_uuid)
        page = self.paginate_queryset(customer_appointments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(customer_appointments, many=True)
        return Response(serializer.data)
