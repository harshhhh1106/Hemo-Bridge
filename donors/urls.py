from django.urls import path

from . import views


urlpatterns = [
    path(
        "register/",
        views.donor_register,
        name="donor_register"
    ),

    path(
        "management/",
        views.donor_management,
        name="donor_management"
    ),
]