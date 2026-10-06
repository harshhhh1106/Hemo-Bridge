from django.contrib import admin
from django.urls import include, path

from .views import home


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        home,
        name="home"
    ),

    path(
        "donors/",
        include("donors.urls")
    ),

    path(
        "bloodbank/",
        include("bloodbank.urls")
    ),

   
    path(
        "requests/",
        include("requests.urls")
    ),

]