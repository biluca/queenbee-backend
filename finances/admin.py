from django.contrib import admin
from .models import Order, OrderItem, OrderType, PaymentType, OrderItemLine


@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'type', 'created_at', 'updated_at']
    list_filter = ['type', 'created_at', 'updated_at']
    search_fields = ['type']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'type', 'created_at', 'updated_at']
    list_filter = ['type', 'created_at', 'updated_at']
    search_fields = ['type']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'uuid', 'description', 'inventory_quantity', 'unit_price', 
        'created_at', 'updated_at'
    ]
    list_filter = ['inventory_quantity', 'unit_price', 'created_at', 'updated_at']
    search_fields = ['description']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'description')
        }),
        ('Inventory & Pricing', {
            'fields': ('inventory_quantity', 'unit_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    # Add filters for low stock
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset
    
    # Custom admin actions
    actions = ['mark_as_low_stock', 'update_stock']
    
    def mark_as_low_stock(self, request, queryset):
        """Mark selected items as low stock"""
        low_stock_count = queryset.filter(inventory_quantity__lt=5).count()
        self.message_user(request, f"{low_stock_count} items have low stock (< 5)")
    mark_as_low_stock.short_description = "Check for low stock items"


@admin.register(OrderItemLine)
class OrderItemLineAdmin(admin.ModelAdmin):
    list_display = [
        'uuid', 'order', 'order_item', 'quantity', 'unit_price', 
        'total_price', 'created_at', 'updated_at'
    ]
    list_filter = [
        'order__order_type__type', 'quantity', 'unit_price', 
        'created_at', 'updated_at'
    ]
    search_fields = [
        'order__uuid', 'order_item__description', 
        'order__customer__first_name', 'order__customer__last_name'
    ]
    readonly_fields = ['uuid', 'total_price', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'order', 'order_item')
        }),
        ('Quantity & Pricing', {
            'fields': ('quantity', 'unit_price', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('order', 'order_item', 'order__customer')


class OrderItemLineInline(admin.TabularInline):
    """Inline for OrderItemLine in Order admin"""
    model = OrderItemLine
    extra = 1
    readonly_fields = ['uuid', 'total_price', 'created_at', 'updated_at']
    fields = ['order_item', 'quantity', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'uuid', 'customer', 'order_type', 'payment_type', 'total', 
        'appointment', 'created_at', 'updated_at'
    ]
    list_filter = [
        'order_type__type', 'payment_type__type', 'total', 
        'created_at', 'updated_at'
    ]
    search_fields = [
        'customer__first_name', 'customer__last_name', 'customer__email',
        'uuid', 'appointment__uuid'
    ]
    readonly_fields = ['uuid', 'created_at', 'updated_at', 'customer_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'customer', 'customer_name')
        }),
        ('Order Details', {
            'fields': ('order_type', 'payment_type', 'total')
        }),
        ('Related Information', {
            'fields': ('appointment',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    # Include order items inline
    inlines = [OrderItemLineInline]
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'customer', 'order_type', 'payment_type', 'appointment'
        ).prefetch_related('order_items')
    
    def customer_name(self, obj):
        """Display customer full name"""
        return obj.customer.full_name if obj.customer else None
    customer_name.short_description = 'Customer Name'
    
    # Custom admin actions
    actions = ['calculate_totals', 'export_orders']
    
    def calculate_totals(self, request, queryset):
        """Calculate and display totals for selected orders"""
        total_amount = sum(order.total for order in queryset)
        income_total = sum(
            order.total for order in queryset 
            if order.order_type.type == 'Income'
        )
        expense_total = sum(
            order.total for order in queryset 
            if order.order_type.type == 'Expense'
        )
        
        self.message_user(
            request, 
            f"Selected orders: Total=${total_amount}, "
            f"Income=${income_total}, Expense=${expense_total}, "
            f"Net=${income_total - expense_total}"
        )
    calculate_totals.short_description = "Calculate totals for selected orders"
