from django.urls import path

from . import views


urlpatterns = [

    path(
        "register/",
        views.donor_register,
        name="donor_register"
    ),

    path(
        "success/",
        views.donor_success,
        name="donor_success"
    ),

]