from django.contrib import admin
from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "registration_number",
        "city",
        "is_verified",
    )

    list_filter = (
        "city",
        "is_verified",
    )

    search_fields = (
        "name",
        "registration_number",
        "email",
    )