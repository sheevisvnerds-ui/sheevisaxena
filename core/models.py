from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        AGENT = 'AGENT', 'Pickup Agent'
        ADMIN = 'ADMIN', 'Admin'

    base_role = Role.CUSTOMER
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CUSTOMER)
    name = models.CharField(max_length=255, verbose_name="Full Name")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class ScrapCategory(models.Model):
    name = models.CharField(max_length=100)
    rate_per_kg = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per Kg in INR")
    image = models.ImageField(upload_to='scrap_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - ₹{self.rate_per_kg}/kg"

class PickupRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ASSIGNED = 'ASSIGNED', 'Assigned'
        COLLECTED = 'COLLECTED', 'Collected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_requests', limit_choices_to={'role': User.Role.CUSTOMER})
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_pickups', limit_choices_to={'role': User.Role.AGENT})
    scrap_category = models.ForeignKey(ScrapCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='pickup_requests')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    scheduled_date = models.DateTimeField()
    address = models.TextField()
    estimated_weight = models.FloatField(help_text="Estimated weight in Kg")
    
    # Filled by Agent
    actual_weight = models.FloatField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pickup #{self.id} - {self.customer.username} ({self.status})"
