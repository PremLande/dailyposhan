from django.db import models
from django.utils import timezone
import uuid
import random
import string


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending COD', 'Pending COD'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
        ('upi', 'UPI'),
    ]

    id = models.CharField(max_length=50, primary_key=True, editable=False)
    customer_name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=20, null=False)
    address = models.TextField(null=False)
    total = models.IntegerField(null=False)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, null=False)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, null=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['customer_name']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate unique order ID: DP{YYMMDD}{XXXX}
            # Format: DP + Year(2) + Month(2) + Day(2) + Random(4)
            now = timezone.now()
            date_part = now.strftime('%y%m%d')  # YYMMDD format
            random_part = ''.join(random.choices(string.digits, k=4))  # 4-digit random number
            self.id = f"DP{date_part}{random_part}"
            
            # Ensure uniqueness by checking if this ID already exists
            while Order.objects.filter(id=self.id).exists():
                random_part = ''.join(random.choices(string.digits, k=4))
                self.id = f"DP{date_part}{random_part}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField(null=False)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_items'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product_id']),
        ]

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in Order {self.order_id}"
