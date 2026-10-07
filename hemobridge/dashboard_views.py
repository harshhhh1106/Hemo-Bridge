from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction, models
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from donors.models import Donor
from bloodbank.models import BloodInventory
from hospitals.models import Hospital
from requests.models import BloodRequest


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@staff_member_required
def dashboard(request):

    total_donors = Donor.objects.count()

    total_hospitals = Hospital.objects.count()

    total_requests = BloodRequest.objects.count()

    pending_requests = BloodRequest.objects.filter(
        status="Pending"
    ).count()

    emergency_requests = BloodRequest.objects.filter(
        urgency="Emergency",
        status="Pending"
    ).count()

    total_blood_units = (
        BloodInventory.objects.aggregate(
            total=Sum("units_available")
        )["total"] or 0
    )

    blood_inventory = (
        BloodInventory.objects
        .all()
        .order_by("blood_group")
    )

    low_stock_blood = (
        BloodInventory.objects
        .filter(units_available__lt=10)
        .order_by("units_available")
    )

    emergency_pending = (
        BloodRequest.objects
        .filter(
            urgency="Emergency",
            status="Pending"
        )
        .select_related("hospital")
        .order_by("-request_date")
    )

    recent_requests = (
        BloodRequest.objects
        .select_related("hospital")
        .order_by("-request_date")[:10]
    )

    context = {
        "total_donors": total_donors,
        "total_hospitals": total_hospitals,
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "emergency_requests": emergency_requests,
        "total_blood_units": total_blood_units,
        "blood_inventory": blood_inventory,
        "low_stock_blood": low_stock_blood,
        "emergency_pending": emergency_pending,
        "recent_requests": recent_requests,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# ============================================================
# REQUEST MANAGEMENT
# ============================================================

@staff_member_required
def dashboard_requests(request):

    # --------------------------------------------------------
    # BASE QUERY
    #
    # Pending requests are shown first.
    #
    # Priority:
    # 1. Emergency
    # 2. Urgent
    # 3. Normal
    #
    # After pending requests, approved/rejected/completed
    # requests are shown.
    # --------------------------------------------------------

    blood_requests = (
        BloodRequest.objects
        .select_related("hospital")
        .order_by(
            models.Case(
                models.When(
                    status="Pending",
                    then=0
                ),
                default=1,
                output_field=models.IntegerField(),
            ),

            models.Case(
                models.When(
                    status="Pending",
                    urgency="Emergency",
                    then=0
                ),
                models.When(
                    status="Pending",
                    urgency="Urgent",
                    then=1
                ),
                models.When(
                    status="Pending",
                    urgency="Normal",
                    then=2
                ),
                default=3,
                output_field=models.IntegerField(),
            ),

            "-request_date",
        )
    )

    # --------------------------------------------------------
    # GET FILTER VALUES
    # --------------------------------------------------------

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    selected_status = request.GET.get(
        "status",
        ""
    )

    selected_urgency = request.GET.get(
        "urgency",
        ""
    )

    selected_blood_group = request.GET.get(
        "blood_group",
        ""
    )

    # --------------------------------------------------------
    # SEARCH BY PATIENT OR HOSPITAL
    # --------------------------------------------------------

    if search_query:

        blood_requests = blood_requests.filter(
            models.Q(
                patient_name__icontains=search_query
            )
            |
            models.Q(
                hospital__name__icontains=search_query
            )
        )

    # --------------------------------------------------------
    # STATUS FILTER
    # --------------------------------------------------------

    if selected_status:

        blood_requests = blood_requests.filter(
            status=selected_status
        )

    # --------------------------------------------------------
    # URGENCY FILTER
    # --------------------------------------------------------

    if selected_urgency:

        blood_requests = blood_requests.filter(
            urgency=selected_urgency
        )

    # --------------------------------------------------------
    # BLOOD GROUP FILTER
    # --------------------------------------------------------

    if selected_blood_group:

        blood_requests = blood_requests.filter(
            blood_group=selected_blood_group
        )

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = {
        "blood_requests": blood_requests,

        "search_query": search_query,

        "selected_status": selected_status,

        "selected_urgency": selected_urgency,

        "selected_blood_group": selected_blood_group,
    }

    return render(
        request,
        "dashboard/requests.html",
        context
    )


# ============================================================
# APPROVE REQUEST
# ============================================================

@staff_member_required
def approve_dashboard_request(
    request,
    request_id
):

    # Only POST requests are allowed.

    if request.method != "POST":

        return redirect(
            "dashboard_requests"
        )

    # Get requested blood request.

    blood_request = get_object_or_404(
        BloodRequest,
        id=request_id
    )

    # --------------------------------------------------------
    # CHECK STATUS
    # --------------------------------------------------------

    if blood_request.status != "Pending":

        messages.warning(
            request,

            f"{blood_request.patient_name}'s request "
            f"is already {blood_request.status}."
        )

        return redirect(
            "dashboard_requests"
        )

    # --------------------------------------------------------
    # APPROVE REQUEST AND UPDATE INVENTORY
    # --------------------------------------------------------

    try:

        with transaction.atomic():

            # Lock inventory row while updating.

            inventory = (
                BloodInventory.objects
                .select_for_update()
                .get(
                    blood_group=blood_request.blood_group
                )
            )

            # ------------------------------------------------
            # CHECK BLOOD AVAILABILITY
            # ------------------------------------------------

            if (
                inventory.units_available
                < blood_request.units_required
            ):

                messages.error(
                    request,

                    f"Not enough "
                    f"{blood_request.blood_group} blood "
                    f"available for "
                    f"{blood_request.patient_name}. "

                    f"Available: "
                    f"{inventory.units_available} units, "

                    f"Required: "
                    f"{blood_request.units_required} units."
                )

                return redirect(
                    "dashboard_requests"
                )

            # ------------------------------------------------
            # DEDUCT REQUIRED UNITS
            # ------------------------------------------------

            inventory.units_available -= (
                blood_request.units_required
            )

            inventory.save()

            # ------------------------------------------------
            # UPDATE REQUEST STATUS
            # ------------------------------------------------

            blood_request.status = "Approved"

            blood_request.save()

        # ----------------------------------------------------
        # SUCCESS MESSAGE
        # ----------------------------------------------------

        messages.success(
            request,

            f"Blood request for "
            f"{blood_request.patient_name} "
            f"was approved successfully. "

            f"{blood_request.units_required} "
            f"unit(s) of "
            f"{blood_request.blood_group} "
            f"deducted from inventory."
        )

    except BloodInventory.DoesNotExist:

        messages.error(
            request,

            f"No inventory record found for "
            f"{blood_request.blood_group}."
        )

    return redirect(
        "dashboard_requests"
    )


# ============================================================
# REJECT REQUEST
# ============================================================

@staff_member_required
def reject_dashboard_request(
    request,
    request_id
):

    # Only POST requests are allowed.

    if request.method != "POST":

        return redirect(
            "dashboard_requests"
        )

    # Get requested blood request.

    blood_request = get_object_or_404(
        BloodRequest,
        id=request_id
    )

    # --------------------------------------------------------
    # CHECK STATUS
    # --------------------------------------------------------

    if blood_request.status != "Pending":

        messages.warning(
            request,

            f"{blood_request.patient_name}'s request "
            f"is already {blood_request.status}."
        )

        return redirect(
            "dashboard_requests"
        )

    # --------------------------------------------------------
    # REJECT REQUEST
    # --------------------------------------------------------

    blood_request.status = "Rejected"

    blood_request.save()

    # --------------------------------------------------------
    # SUCCESS MESSAGE
    # --------------------------------------------------------

    messages.success(
        request,

        f"Blood request for "
        f"{blood_request.patient_name} "
        f"was rejected."
    )

    return redirect(
        "dashboard_requests"
    )