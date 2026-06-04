from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='customer', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.name} ({self.email})"

    def set_password(self, raw_password):
        """Hash and set password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verify password against hash"""
        return check_password(raw_password, self.password)
