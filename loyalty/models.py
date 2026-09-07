from django.db import models
from django.utils.crypto import get_random_string
from django.urls import reverse
from reputation.models import StaffMember

class LoyaltyMember(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    total_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Track who faciliated the sign-up
    facilitated_by = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='facilitated_signups')

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = get_random_string(8).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} ({self.referral_code})"

class CrewWallet(models.Model):
    staff_member = models.OneToOneField(StaffMember, on_delete=models.CASCADE, related_name='wallet')
    available_points = models.PositiveIntegerField(default=0)
    total_earned_points = models.PositiveIntegerField(default=0)
    total_cash_redeemed = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet: {self.staff_member.name}"

class PointTransaction(models.Model):
    SOURCE_CHOICES = [
        ('REVIEW', 'Review Received'),
        ('SIGNUP', 'Loyalty Sign-up Facilitated'),
        ('REDEMPTION', 'Cash Redemption'),
    ]
    
    wallet = models.ForeignKey(CrewWallet, on_delete=models.CASCADE, related_name='transactions')
    points = models.IntegerField() # Negative for redemptions
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.staff_member.name}: {self.points} ({self.source})"

class Referral(models.Model):
    referrer = models.ForeignKey(LoyaltyMember, on_delete=models.CASCADE, related_name='referrals')
    referred_customer_name = models.CharField(max_length=100)
    booking = models.OneToOneField('bookings.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.customer_name} referred {self.referred_customer_name}"

class RedemptionRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    wallet = models.ForeignKey(CrewWallet, on_delete=models.CASCADE, related_name='redemptions')
    points_to_redeem = models.PositiveIntegerField()
    cash_value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.wallet.staff_member.name}: {self.points_to_redeem} pts"
