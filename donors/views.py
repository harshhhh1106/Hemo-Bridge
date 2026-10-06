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