from django.shortcuts import render, redirect

from .forms import DonorForm


def donor_register(request):

    if request.method == "POST":

        form = DonorForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("donor_success")

    else:

        form = DonorForm()

    return render(
        request,
        "donors/donor_register.html",
        {
            "form": form
        }
    )


def donor_success(request):

    return render(
        request,
        "donors/donor_success.html"
    )
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import Donor


@staff_member_required
def donor_management(request):

    # ========================================================
    # DONOR STATISTICS
    # ========================================================

    total_donors = Donor.objects.count()

    available_donors = Donor.objects.filter(
        is_available=True
    ).count()

    unavailable_donors = Donor.objects.filter(
        is_available=False
    ).count()

    blood_groups_count = (
        Donor.objects
        .values("blood_group")
        .distinct()
        .count()
    )


    # ========================================================
    # DONOR LIST
    # ========================================================

    donors = (
        Donor.objects
        .all()
        .order_by("-created_at")
    )


    # ========================================================
    # FILTER VALUES
    # ========================================================

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    selected_blood_group = request.GET.get(
        "blood_group",
        ""
    )

    selected_city = request.GET.get(
        "city",
        ""
    ).strip()

    selected_availability = request.GET.get(
        "availability",
        ""
    )


    # ========================================================
    # SEARCH
    # ========================================================

    if search_query:

        from django.db.models import Q

        donors = donors.filter(
            Q(name__icontains=search_query)
            |
            Q(email__icontains=search_query)
            |
            Q(phone__icontains=search_query)
            |
            Q(city__icontains=search_query)
        )


    # ========================================================
    # BLOOD GROUP FILTER
    # ========================================================

    if selected_blood_group:

        donors = donors.filter(
            blood_group=selected_blood_group
        )


    # ========================================================
    # CITY FILTER
    # ========================================================

    if selected_city:

        donors = donors.filter(
            city__icontains=selected_city
        )


    # ========================================================
    # AVAILABILITY FILTER
    # ========================================================

    if selected_availability == "available":

        donors = donors.filter(
            is_available=True
        )

    elif selected_availability == "unavailable":

        donors = donors.filter(
            is_available=False
        )


    # ========================================================
    # CONTEXT
    # ========================================================

    context = {

        "donors": donors,

        "total_donors": total_donors,

        "available_donors": available_donors,

        "unavailable_donors": unavailable_donors,

        "blood_groups_count": blood_groups_count,

        "search_query": search_query,

        "selected_blood_group":
            selected_blood_group,

        "selected_city":
            selected_city,

        "selected_availability":
            selected_availability,
    }


    return render(
        request,
        "dashboard/donors.html",
        context
    )