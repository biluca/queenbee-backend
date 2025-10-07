from django.contrib import admin
from .models import Customer, AppointmentType, Appointment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'uuid', 'first_name', 'last_name', 'email', 'phone', 
        'is_active', 'created_at', 'updated_at'
    ]
    list_filter = [
        'is_active', 'gender', 'address_country', 'address_state', 
        'created_at', 'updated_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'nickname', 'email', 'phone',
        'address_city', 'address_state', 'address_country'
    ]
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'uuid', 'first_name', 'last_name', 'nickname', 
                'email', 'phone', 'date_of_birth', 'gender'
            )
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
        ('Address', {
            'fields': (
                'address_street', 'address_number', 'address_neighborhood',
                'address_city', 'address_state', 'address_zip_code', 'address_country'
            )
        }),
        ('Preferences & Tags', {
            'fields': ('preferences', 'tags')
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related()


@admin.register(AppointmentType)
class AppointmentTypeAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['description']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'uuid', 'customer', 'appointment_type', 'start_time', 'end_time', 
        'status', 'created_at', 'updated_at'
    ]
    list_filter = [
        'status', 'appointment_type', 'start_time', 'end_time', 
        'created_at', 'updated_at'
    ]
    search_fields = [
        'customer__first_name', 'customer__last_name', 'customer__email',
        'appointment_type__description', 'notes'
    ]
    readonly_fields = ['uuid', 'created_at', 'updated_at', 'duration_minutes']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'customer', 'appointment_type')
        }),
        ('Schedule', {
            'fields': ('start_time', 'end_time', 'duration_minutes', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes', 'cancellation_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'start_time'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('customer', 'appointment_type')
