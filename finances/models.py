import uuid
from django.db import models
from django.core.validators import MinValueValidator
from customer_relationship.models import BaseModel, Customer


class OrderType(BaseModel):
    """Model for order types (Income/Expense)"""
    
    TYPE_CHOICES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    class Meta:
        db_table = "order_types"
        ordering = ["type"]
        verbose_name = "Order Type"
        verbose_name_plural = "Order Types"
    
    def __str__(self):
        return self.type


class PaymentType(BaseModel):
    """Model for payment types"""
    
    TYPE_CHOICES = [
        ("Cash", "Cash"),
        ("Credit Card", "Credit Card"),
        ("Debit Card", "Debit Card"),
        ("Exchange", "Exchange"),
        ("Bank Slip", "Bank Slip"),
        ("Pix", "Pix"),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    class Meta:
        db_table = "payment_types"
        ordering = ["type"]
        verbose_name = "Payment Type"
        verbose_name_plural = "Payment Types"
    
    def __str__(self):
        return self.type


class OrderItem(BaseModel):
    """Model for order items/products"""
    
    description = models.CharField(max_length=255)
    inventory_quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        db_table = "order_items"
        ordering = ["description"]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return f"{self.description} - ${self.unit_price}"


class Order(BaseModel):
    """Model for orders"""
    
    # Foreign Key relationships
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )
    order_type = models.ForeignKey(
        OrderType, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )
    payment_type = models.ForeignKey(
        PaymentType, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )
    
    # Optional appointment reference
    appointment = models.ForeignKey(
        'customer_relationship.Appointment', 
        on_delete=models.SET_NULL, 
        related_name="orders",
        blank=True, 
        null=True
    )
    
    # Order details
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order {self.uuid} - {self.customer.full_name} - ${self.total}"
    
    @property
    def customer_name(self):
        return self.customer.full_name if self.customer else None


class OrderItemLine(BaseModel):
    """Model for order item lines (items within an order)"""
    
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="order_items"
    )
    order_item = models.ForeignKey(
        OrderItem, 
        on_delete=models.CASCADE, 
        related_name="order_lines"
    )
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        db_table = "order_item_lines"
        ordering = ["order", "order_item"]
        verbose_name = "Order Item Line"
        verbose_name_plural = "Order Item Lines"
    
    def __str__(self):
        return f"{self.order_item.description} x{self.quantity} - ${self.total_price}"
    
    def save(self, *args, **kwargs):
        """Calculate total_price automatically"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
