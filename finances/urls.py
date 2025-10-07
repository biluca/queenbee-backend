from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, OrderTypeViewSet, PaymentTypeViewSet, OrderItemLineViewSet

# Create a router and register the ViewSets
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'order-types', OrderTypeViewSet, basename='order-type')
router.register(r'payment-types', PaymentTypeViewSet, basename='payment-type')
router.register(r'order-item-lines', OrderItemLineViewSet, basename='order-item-line')

app_name = 'finances'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
]

# Available API endpoints:

# ORDER TYPES:
# GET /api/order-types/ - List all order types (with pagination, filtering, search)
# POST /api/order-types/ - Create a new order type
# GET /api/order-types/{uuid}/ - Retrieve a specific order type
# PUT /api/order-types/{uuid}/ - Update a specific order type (full update)
# PATCH /api/order-types/{uuid}/ - Partial update a specific order type
# DELETE /api/order-types/{uuid}/ - Delete a specific order type

# PAYMENT TYPES:
# GET /api/payment-types/ - List all payment types (with pagination, filtering, search)
# POST /api/payment-types/ - Create a new payment type
# GET /api/payment-types/{uuid}/ - Retrieve a specific payment type
# PUT /api/payment-types/{uuid}/ - Update a specific payment type (full update)
# PATCH /api/payment-types/{uuid}/ - Partial update a specific payment type
# DELETE /api/payment-types/{uuid}/ - Delete a specific payment type

# ORDER ITEMS:
# GET /api/order-items/ - List all order items (with pagination, filtering, search)
# POST /api/order-items/ - Create a new order item
# GET /api/order-items/{uuid}/ - Retrieve a specific order item
# PUT /api/order-items/{uuid}/ - Update a specific order item (full update)
# PATCH /api/order-items/{uuid}/ - Partial update a specific order item
# DELETE /api/order-items/{uuid}/ - Delete a specific order item
# GET /api/order-items/low_stock/ - List items with low inventory

# ORDER ITEM LINES:
# GET /api/order-item-lines/ - List all order item lines (with pagination, filtering, search)
# POST /api/order-item-lines/ - Create a new order item line
# GET /api/order-item-lines/{uuid}/ - Retrieve a specific order item line
# PUT /api/order-item-lines/{uuid}/ - Update a specific order item line (full update)
# PATCH /api/order-item-lines/{uuid}/ - Partial update a specific order item line
# DELETE /api/order-item-lines/{uuid}/ - Delete a specific order item line

# ORDERS:
# GET /api/orders/ - List all orders (with pagination, filtering, search)
# POST /api/orders/ - Create a new order
# GET /api/orders/{uuid}/ - Retrieve a specific order
# PUT /api/orders/{uuid}/ - Update a specific order (full update)
# PATCH /api/orders/{uuid}/ - Partial update a specific order
# DELETE /api/orders/{uuid}/ - Delete a specific order
# GET /api/orders/today/ - List orders created today
# GET /api/orders/this_month/ - List orders created this month
# GET /api/orders/by_customer/ - Get orders for a specific customer (requires ?customer_uuid= parameter)
# GET /api/orders/income/ - List income orders
# GET /api/orders/expense/ - List expense orders
# POST /api/orders/create_with_items/ - Create order with items in single request
# GET /api/orders/statistics/ - Get order statistics

# Query parameters for filtering:
# Order Types: ?type=Income/Expense
# Payment Types: ?type=Cash/Credit Card/etc
# Order Items: ?inventory_quantity=0, ?search=description
# Orders: ?order_type={uuid}, ?payment_type={uuid}, ?customer={uuid}, ?appointment={uuid}
# ?search=term (searches customer name/email)
# ?ordering=created_at,-updated_at,total (for orders)

# Advanced search query parameters:
# Order by customer: ?customer_uuid={uuid} (for by_customer endpoint)
# Order statistics: No parameters needed, returns comprehensive stats