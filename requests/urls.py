from django.urls import path

from . import views


urlpatterns = [

    path(
        "request/",
        views.blood_request,
        name="blood_request"
    ),

    path(
        "success/",
        views.request_success,
        name="request_success"
    ),

]