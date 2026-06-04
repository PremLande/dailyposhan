from django.db import models
import uuid


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]
    
    METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
        ('upi', 'UPI'),
    ]

    id = models.CharField(max_length=50, primary_key=True, editable=False)
    order_id = models.CharField(max_length=50, null=False)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, null=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=False)
    amount = models.IntegerField(null=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['status']),
            models.Index(fields=['method']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"PAY{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.id} - {self.method}"


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=20, null=False)
    full_address = models.TextField(null=False)
    pincode = models.CharField(max_length=10, null=False)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'addresses'
        indexes = [
            models.Index(fields=['customer_name']),
            models.Index(fields=['pincode']),
            models.Index(fields=['is_default']),
        ]

    def __str__(self):
        return f"{self.customer_name} - {self.pincode}"
