from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class Student(models.Model):
    """Student model for laundry service"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrollment_no = models.CharField(max_length=20, unique=True)
    phone_no = models.CharField(max_length=15)
    bag_no = models.CharField(
        max_length=20,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^[BG]-\d+$',
                message='Bag number must start with B- or G- followed by numbers',
                code='invalid_bag_number'
            )
        ]
    )
    residency_no = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.enrollment_no}"
    
    def save(self, *args, **kwargs):
        # Auto-generate bag number if not provided
        if not self.bag_no:
            self.bag_no = f"BAG{self.enrollment_no}"
        super().save(*args, **kwargs)

class Washerman(models.Model):
    """Washerman model for laundry service"""
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Will be hashed
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Washerman - {self.username}"

class Order(models.Model):
    """Laundry order model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('inprogress', 'In Progress'),
        ('complete', 'Complete'),
    ]
    
    bag_no = models.CharField(max_length=20)
    number_of_clothes = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.bag_no} - {self.status}"
