from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import Hospital

@staff_member_required
def hospital_management(request):

    # ========================================================
    # HOSPITAL STATISTICS
    # ========================================================

    total_hospitals = Hospital.objects.count()

    verified_hospitals = Hospital.objects.filter(
        is_verified=True
    ).count()

    unverified_hospitals = Hospital.objects.filter(
        is_verified=False
    ).count()

    # ========================================================
    # HOSPITAL LIST
    # ========================================================

    hospitals = (
        Hospital.objects
        .annotate(
            request_count=Count(
                "blood_requests"
            )
        )
        .order_by("-created_at")
    )

    # ========================================================
    # FILTER VALUES
    # ========================================================

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    selected_city = request.GET.get(
        "city",
        ""
    ).strip()

    selected_verification = request.GET.get(
        "verification",
        ""
    )

    # ========================================================
    # SEARCH
    # ========================================================

    if search_query:

        hospitals = hospitals.filter(
            Q(name__icontains=search_query)
            |
            Q(registration_number__icontains=search_query)
            |
            Q(email__icontains=search_query)
            |
            Q(phone__icontains=search_query)
            |
            Q(city__icontains=search_query)
        )

    # ========================================================
    # CITY FILTER
    # ========================================================

    if selected_city:

        hospitals = hospitals.filter(
            city__icontains=selected_city
        )

    # ========================================================
    # VERIFICATION FILTER
    # ========================================================

    if selected_verification == "verified":

        hospitals = hospitals.filter(
            is_verified=True
        )

    elif selected_verification == "unverified":

        hospitals = hospitals.filter(
            is_verified=False
        )

    # ========================================================
    # CONTEXT
    # ========================================================

    context = {

        "hospitals": hospitals,

        "total_hospitals": total_hospitals,

        "verified_hospitals":
            verified_hospitals,

        "unverified_hospitals":
            unverified_hospitals,

        "search_query":
            search_query,

        "selected_city":
            selected_city,

        "selected_verification":
            selected_verification,
    }

    return render(
        request,
        "dashboard/hospitals.html",
        context
    )
    from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect


@staff_member_required
def hospital_detail(request, hospital_id):

    hospital = get_object_or_404(
        Hospital,
        id=hospital_id
    )

    return render(
        request,
        "dashboard/hospital_detail.html",
        {
            "hospital": hospital
        }
    )


@staff_member_required
def toggle_hospital_verification(
    request,
    hospital_id
):

    if request.method != "POST":

        return redirect(
            "hospital_management"
        )

    hospital = get_object_or_404(
        Hospital,
        id=hospital_id
    )

    if hospital.is_verified:

        hospital.is_verified = False

        hospital.save()

        messages.warning(
            request,
            f"{hospital.name} has been marked as unverified."
        )

    else:

        hospital.is_verified = True

        hospital.save()

        messages.success(
            request,
            f"{hospital.name} has been verified successfully."
        )

    return redirect(
        "hospital_management"
    )