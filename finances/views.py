from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Order, OrderItem, OrderType, PaymentType, OrderItemLine
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer, OrderWithItemsCreateSerializer,
    OrderItemSerializer, OrderItemCreateSerializer, OrderItemUpdateSerializer,
    OrderTypeSerializer, OrderTypeCreateSerializer, OrderTypeUpdateSerializer,
    PaymentTypeSerializer, PaymentTypeCreateSerializer, PaymentTypeUpdateSerializer,
    OrderItemLineSerializer, OrderItemLineCreateSerializer, OrderItemLineUpdateSerializer
)


class OrderTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OrderType CRUD operations
    
    Provides:
    - GET /api/order-types/ - List all order types (with pagination, filtering, search)
    - POST /api/order-types/ - Create a new order type
    - GET /api/order-types/{uuid}/ - Retrieve a specific order type
    - PUT /api/order-types/{uuid}/ - Update a specific order type (full update)
    - PATCH /api/order-types/{uuid}/ - Partial update a specific order type
    - DELETE /api/order-types/{uuid}/ - Delete a specific order type
    """
    
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer
    lookup_field = 'uuid'
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['type']
    ordering_fields = ['created_at', 'updated_at', 'type']
    ordering = ['type']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return OrderTypeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderTypeUpdateSerializer
        return OrderTypeSerializer


class PaymentTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PaymentType CRUD operations
    
    Provides:
    - GET /api/payment-types/ - List all payment types (with pagination, filtering, search)
    - POST /api/payment-types/ - Create a new payment type
    - GET /api/payment-types/{uuid}/ - Retrieve a specific payment type
    - PUT /api/payment-types/{uuid}/ - Update a specific payment type (full update)
    - PATCH /api/payment-types/{uuid}/ - Partial update a specific payment type
    - DELETE /api/payment-types/{uuid}/ - Delete a specific payment type
    """
    
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer
    lookup_field = 'uuid'
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['type']
    ordering_fields = ['created_at', 'updated_at', 'type']
    ordering = ['type']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return PaymentTypeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PaymentTypeUpdateSerializer
        return PaymentTypeSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OrderItem CRUD operations
    
    Provides:
    - GET /api/order-items/ - List all order items (with pagination, filtering, search)
    - POST /api/order-items/ - Create a new order item
    - GET /api/order-items/{uuid}/ - Retrieve a specific order item
    - PUT /api/order-items/{uuid}/ - Update a specific order item (full update)
    - PATCH /api/order-items/{uuid}/ - Partial update a specific order item
    - DELETE /api/order-items/{uuid}/ - Delete a specific order item
    
    Additional endpoints:
    - GET /api/order-items/low_stock/ - List items with low inventory
    """
    
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'uuid'
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['inventory_quantity']
    search_fields = ['description']
    ordering_fields = ['created_at', 'updated_at', 'description', 'unit_price', 'inventory_quantity']
    ordering = ['description']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return OrderItemCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderItemUpdateSerializer
        return OrderItemSerializer
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get order items with low inventory (less than 5)"""
        low_stock_items = self.queryset.filter(inventory_quantity__lt=5)
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)


class OrderItemLineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OrderItemLine CRUD operations
    
    Provides:
    - GET /api/order-item-lines/ - List all order item lines (with pagination, filtering, search)
    - POST /api/order-item-lines/ - Create a new order item line
    - GET /api/order-item-lines/{uuid}/ - Retrieve a specific order item line
    - PUT /api/order-item-lines/{uuid}/ - Update a specific order item line (full update)
    - PATCH /api/order-item-lines/{uuid}/ - Partial update a specific order item line
    - DELETE /api/order-item-lines/{uuid}/ - Delete a specific order item line
    """
    
    queryset = OrderItemLine.objects.all()
    serializer_class = OrderItemLineSerializer
    lookup_field = 'uuid'
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['order', 'order_item', 'quantity']
    search_fields = ['order_item__description']
    ordering_fields = ['created_at', 'updated_at', 'quantity', 'unit_price', 'total_price']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Override queryset to include related objects"""
        return self.queryset.select_related('order', 'order_item')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return OrderItemLineCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderItemLineUpdateSerializer
        return OrderItemLineSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order CRUD operations
    
    Provides:
    - GET /api/orders/ - List all orders (with pagination, filtering, search)
    - POST /api/orders/ - Create a new order
    - GET /api/orders/{uuid}/ - Retrieve a specific order
    - PUT /api/orders/{uuid}/ - Update a specific order (full update)
    - PATCH /api/orders/{uuid}/ - Partial update a specific order
    - DELETE /api/orders/{uuid}/ - Delete a specific order
    
    Additional endpoints:
    - GET /api/orders/today/ - List orders created today
    - GET /api/orders/this_month/ - List orders created this month
    - GET /api/orders/by_customer/ - Get orders for a specific customer
    - GET /api/orders/income/ - List income orders
    - GET /api/orders/expense/ - List expense orders
    - POST /api/orders/create_with_items/ - Create order with items in single request
    - GET /api/orders/statistics/ - Get order statistics
    """
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'uuid'
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['order_type', 'payment_type', 'customer', 'appointment']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email']
    ordering_fields = ['created_at', 'updated_at', 'total']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Override queryset to include related objects"""
        return self.queryset.select_related(
            'customer', 'order_type', 'payment_type', 'appointment'
        ).prefetch_related('order_items__order_item')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'create_with_items':
            return OrderWithItemsCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get orders created today"""
        today = timezone.now().date()
        today_orders = self.get_queryset().filter(created_at__date=today)
        serializer = self.get_serializer(today_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def this_month(self, request):
        """Get orders created this month"""
        now = timezone.now()
        this_month_orders = self.get_queryset().filter(
            created_at__year=now.year,
            created_at__month=now.month
        )
        serializer = self.get_serializer(this_month_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get orders for a specific customer"""
        customer_uuid = request.query_params.get('customer_uuid')
        if not customer_uuid:
            return Response(
                {'error': 'customer_uuid parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        customer_orders = self.get_queryset().filter(customer__uuid=customer_uuid)
        serializer = self.get_serializer(customer_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def income(self, request):
        """Get income orders"""
        income_orders = self.get_queryset().filter(order_type__type='Income')
        serializer = self.get_serializer(income_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expense(self, request):
        """Get expense orders"""
        expense_orders = self.get_queryset().filter(order_type__type='Expense')
        serializer = self.get_serializer(expense_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def create_with_items(self, request):
        """Create order with order items in a single request"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                OrderSerializer(order, context={'request': request}).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get order statistics"""
        queryset = self.get_queryset()
        
        # Basic counts
        total_orders = queryset.count()
        income_orders = queryset.filter(order_type__type='Income').count()
        expense_orders = queryset.filter(order_type__type='Expense').count()
        
        # Total amounts
        total_income = queryset.filter(order_type__type='Income').aggregate(
            total=Sum('total')
        )['total'] or 0
        total_expense = queryset.filter(order_type__type='Expense').aggregate(
            total=Sum('total')
        )['total'] or 0
        
        # This month stats
        now = timezone.now()
        this_month_orders = queryset.filter(
            created_at__year=now.year,
            created_at__month=now.month
        )
        this_month_income = this_month_orders.filter(order_type__type='Income').aggregate(
            total=Sum('total')
        )['total'] or 0
        this_month_expense = this_month_orders.filter(order_type__type='Expense').aggregate(
            total=Sum('total')
        )['total'] or 0
        
        return Response({
            'total_orders': total_orders,
            'income_orders': income_orders,
            'expense_orders': expense_orders,
            'total_income': total_income,
            'total_expense': total_expense,
            'net_profit': total_income - total_expense,
            'this_month': {
                'orders': this_month_orders.count(),
                'income': this_month_income,
                'expense': this_month_expense,
                'net_profit': this_month_income - this_month_expense,
            }
        })