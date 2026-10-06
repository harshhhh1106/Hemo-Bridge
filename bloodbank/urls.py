from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.blood_availability,
        name="blood_availability"
    ),

]