from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="jobs"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # when job is posted
    updated_at = models.DateTimeField(auto_now=True)      # when job is updated

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("selected", "Selected"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.applicant} applied to {self.job.title}"
