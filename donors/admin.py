from django.contrib import admin
from .models import Donor


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "blood_group",
        "phone",
        "city",
        "is_available",
    )

    list_filter = (
        "blood_group",
        "gender",
        "is_available",
        "city",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )