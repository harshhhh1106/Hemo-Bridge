from django.urls import path

from . import views


urlpatterns = [

    path(
        "management/",
        views.hospital_management,
        name="hospital_management"
    ),

    path(
        "management/<int:hospital_id>/",
        views.hospital_detail,
        name="hospital_detail"
    ),

    path(
        "management/<int:hospital_id>/toggle-verification/",
        views.toggle_hospital_verification,
        name="toggle_hospital_verification"
    ),

]