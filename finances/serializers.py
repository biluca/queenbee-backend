from rest_framework import serializers
from .models import Order, OrderItem, OrderType, PaymentType, OrderItemLine


class OrderTypeSerializer(serializers.ModelSerializer):
    """Serializer for OrderType model"""
    
    class Meta:
        model = OrderType
        fields = ['uuid', 'type', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class OrderTypeCreateSerializer(OrderTypeSerializer):
    """Serializer for creating order types with required fields validation"""
    
    class Meta(OrderTypeSerializer.Meta):
        extra_kwargs = {
            'type': {'required': True},
        }


class OrderTypeUpdateSerializer(OrderTypeSerializer):
    """Serializer for updating order types with optional fields"""
    
    class Meta(OrderTypeSerializer.Meta):
        pass


class PaymentTypeSerializer(serializers.ModelSerializer):
    """Serializer for PaymentType model"""
    
    class Meta:
        model = PaymentType
        fields = ['uuid', 'type', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class PaymentTypeCreateSerializer(PaymentTypeSerializer):
    """Serializer for creating payment types with required fields validation"""
    
    class Meta(PaymentTypeSerializer.Meta):
        extra_kwargs = {
            'type': {'required': True},
        }


class PaymentTypeUpdateSerializer(PaymentTypeSerializer):
    """Serializer for updating payment types with optional fields"""
    
    class Meta(PaymentTypeSerializer.Meta):
        pass


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    
    class Meta:
        model = OrderItem
        fields = ['uuid', 'description', 'inventory_quantity', 'unit_price', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class OrderItemCreateSerializer(OrderItemSerializer):
    """Serializer for creating order items with required fields validation"""
    
    class Meta(OrderItemSerializer.Meta):
        extra_kwargs = {
            'description': {'required': True},
            'unit_price': {'required': True},
        }


class OrderItemUpdateSerializer(OrderItemSerializer):
    """Serializer for updating order items with optional fields"""
    
    class Meta(OrderItemSerializer.Meta):
        pass


class OrderItemLineSerializer(serializers.ModelSerializer):
    """Serializer for OrderItemLine model"""
    order_item_description = serializers.CharField(source='order_item.description', read_only=True)
    
    class Meta:
        model = OrderItemLine
        fields = [
            'uuid', 'order', 'order_item', 'order_item_description', 
            'quantity', 'unit_price', 'total_price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'total_price', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate order item line data"""
        if 'quantity' in data and data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        if 'unit_price' in data and data['unit_price'] < 0:
            raise serializers.ValidationError("Unit price cannot be negative.")
        return data


class OrderItemLineCreateSerializer(OrderItemLineSerializer):
    """Serializer for creating order item lines with required fields validation"""
    
    class Meta(OrderItemLineSerializer.Meta):
        extra_kwargs = {
            'order': {'required': True},
            'order_item': {'required': True},
            'quantity': {'required': True},
            'unit_price': {'required': True},
        }


class OrderItemLineUpdateSerializer(OrderItemLineSerializer):
    """Serializer for updating order item lines with optional fields"""
    
    class Meta(OrderItemLineSerializer.Meta):
        pass


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    order_type_name = serializers.CharField(source='order_type.type', read_only=True)
    payment_type_name = serializers.CharField(source='payment_type.type', read_only=True)
    appointment_info = serializers.SerializerMethodField()
    order_items = OrderItemLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'uuid', 'customer', 'customer_name', 'order_type', 'order_type_name',
            'payment_type', 'payment_type_name', 'appointment', 'appointment_info',
            'total', 'order_items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']
    
    def get_appointment_info(self, obj):
        """Get appointment information if exists"""
        if obj.appointment:
            return {
                'uuid': obj.appointment.uuid,
                'start_time': obj.appointment.start_time,
                'appointment_type': obj.appointment.appointment_type.description
            }
        return None
    
    def validate_total(self, value):
        """Validate total amount"""
        if value < 0:
            raise serializers.ValidationError("Total cannot be negative.")
        return value


class OrderCreateSerializer(OrderSerializer):
    """Serializer for creating orders with required fields validation"""
    
    class Meta(OrderSerializer.Meta):
        extra_kwargs = {
            'customer': {'required': True},
            'order_type': {'required': True},
            'payment_type': {'required': True},
            'total': {'required': True},
        }


class OrderUpdateSerializer(OrderSerializer):
    """Serializer for updating orders with optional fields"""
    
    class Meta(OrderSerializer.Meta):
        pass


class OrderWithItemsCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders with order items in a single request"""
    order_items = OrderItemLineCreateSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'uuid', 'customer', 'order_type', 'payment_type', 
            'appointment', 'order_items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'total', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create order with order items and calculate total"""
        order_items_data = validated_data.pop('order_items')
        
        # Calculate total from order items
        total = sum(
            item_data['quantity'] * item_data['unit_price'] 
            for item_data in order_items_data
        )
        validated_data['total'] = total
        
        # Create the order
        order = Order.objects.create(**validated_data)
        
        # Create order items
        for item_data in order_items_data:
            OrderItemLine.objects.create(order=order, **item_data)
        
        return order
    
    def to_representation(self, instance):
        """Use the full OrderSerializer for representation"""
        return OrderSerializer(instance, context=self.context).data