from django.shortcuts import render

from .models import BloodInventory


def blood_availability(request):

    blood_group = request.GET.get(
        "blood_group",
        ""
    )

    if blood_group:

        blood_inventory = BloodInventory.objects.filter(
            blood_group=blood_group
        )

    else:

        blood_inventory = BloodInventory.objects.all()

    return render(
        request,
        "bloodbank/blood_availability.html",
        {
            "blood_inventory": blood_inventory,
            "selected_blood_group": blood_group,
        }
    )