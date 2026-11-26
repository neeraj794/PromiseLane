from django.db import models
from authen.models import CustomUser

# Create your models here.
class Interest(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
    ]
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sent_interests')
    receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='received_interests')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('sender','receiver')

    def __str__(self):
        return f"{self.sender} -> {self.receiver}({self.status})"


class BlockedUser(models.Model):
    blocker = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='blocked_users')
    blocked = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='blocked_by_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker','blocked')
    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"

class Report(models.Model):
    REASON_CHOICES = [
        ('Fake Profile','Fake Profile'),
        ('Inappropiate Content','Inappropiate Content'),
        ('Harassment','Harassment'),
        ('Suspicious Activity','Suspicious Activity'),
        ('Other','Other')
    ]
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Reviewed','Reviewed'),
        ('Resolved','Resolved')
    ]
    reporter = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='submitted_reports')
    reported_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='reports_received')
    reason = models.CharField(max_length=50,choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.reporter} reported {self.reported_user}"

class PartnerPreFerences(models.Model):
    RELIGION_CHOICES = [
        ('Hindu','Hindu'),
        ('Muslim','Muslim'),
        ('Christian','Christaian'),
        ('Other','Other')
    ]
    MARITAL_STATUS_CHOICES = [
        ('Single','Single'),
        ('Divorced','Divorced'),
        ('Widowed','Widowed'),
    ]
    GENDER_CHOICES = [
        ('Male','Male'),
        ('Female','Female'),
        ('Any','Any')
    ]
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='partner_preferences')
    min_age = models.PositiveIntegerField(default=18)
    max_age = models.PositiveIntegerField(default=40)
    preferred_gender = models.CharField(max_length=10,choices=GENDER_CHOICES,default='Any')
    religion = models.CharField(max_length=30,choices=RELIGION_CHOICES,default='Any')
    marital_status = models.CharField(max_length=30,choices=MARITAL_STATUS_CHOICES,default='Any')
    city = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences of {self.user.username}"