from django.db import models
from hospitals.models import Hospital


class BloodRequest(models.Model):

    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    URGENCY_CHOICES = [
        ("Normal", "Normal"),
        ("Urgent", "Urgent"),
        ("Emergency", "Emergency"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
    ]

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="blood_requests"
    )

    patient_name = models.CharField(
        max_length=100
    )

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES
    )

    units_required = models.PositiveIntegerField()

    urgency = models.CharField(
        max_length=20,
        choices=URGENCY_CHOICES,
        default="Normal"
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    request_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"