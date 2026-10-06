from django.shortcuts import render, redirect

from .forms import BloodRequestForm


def blood_request(request):

    blood_group = request.GET.get(
        "blood_group",
        ""
    )

    if request.method == "POST":

        form = BloodRequestForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("request_success")

    else:

        form = BloodRequestForm(
            blood_group=blood_group
        )

    return render(
        request,
        "requests/blood_request.html",
        {
            "form": form,
            "blood_group": blood_group,
        }
    )


def request_success(request):

    return render(
        request,
        "requests/request_success.html"
    )