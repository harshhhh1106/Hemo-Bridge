from django.contrib import admin, messages
from django.db import transaction

from .models import BloodRequest
from bloodbank.models import BloodInventory


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):

    list_display = (
        "patient_name",
        "hospital",
        "blood_group",
        "units_required",
        "urgency",
        "status",
        "request_date",
    )

    list_filter = (
        "blood_group",
        "urgency",
        "status",
        "request_date",
    )

    search_fields = (
        "patient_name",
        "hospital__name",
        "blood_group",
    )

    ordering = (
        "-request_date",
    )

    actions = [
        "approve_requests",
        "reject_requests",
    ]

    @admin.action(description="Approve selected blood requests")
    def approve_requests(self, request, queryset):

        approved_count = 0

        for blood_request in queryset:

            if blood_request.status != "Pending":
                self.message_user(
                    request,
                    f"{blood_request.patient_name}'s request is already "
                    f"{blood_request.status}.",
                    level=messages.WARNING,
                )
                continue

            try:

                with transaction.atomic():

                    inventory = BloodInventory.objects.select_for_update().get(
                        blood_group=blood_request.blood_group
                    )

                    if inventory.units_available < blood_request.units_required:

                        self.message_user(
                            request,
                            f"Not enough {blood_request.blood_group} blood "
                            f"for {blood_request.patient_name}. "
                            f"Available: {inventory.units_available}, "
                            f"Required: {blood_request.units_required}.",
                            level=messages.ERROR,
                        )

                        continue

                    inventory.units_available -= blood_request.units_required
                    inventory.save()

                    blood_request.status = "Approved"
                    blood_request.save()

                    approved_count += 1

            except BloodInventory.DoesNotExist:

                self.message_user(
                    request,
                    f"No inventory record found for "
                    f"{blood_request.blood_group}.",
                    level=messages.ERROR,
                )

        if approved_count:

            self.message_user(
                request,
                f"{approved_count} blood request(s) approved successfully "
                f"and inventory updated.",
                level=messages.SUCCESS,
            )

    @admin.action(description="Reject selected blood requests")
    def reject_requests(self, request, queryset):

        rejected_count = 0

        for blood_request in queryset:

            if blood_request.status != "Pending":

                self.message_user(
                    request,
                    f"{blood_request.patient_name}'s request is already "
                    f"{blood_request.status}.",
                    level=messages.WARNING,
                )

                continue

            blood_request.status = "Rejected"
            blood_request.save()

            rejected_count += 1

        if rejected_count:

            self.message_user(
                request,
                f"{rejected_count} blood request(s) rejected.",
                level=messages.SUCCESS,
            )