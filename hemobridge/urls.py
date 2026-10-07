from django.contrib import admin
from django.urls import include, path

from .views import home
from .dashboard_views import (
    dashboard,
    dashboard_requests,
    approve_dashboard_request,
    reject_dashboard_request,
)


urlpatterns = [

    # Main Website
    path(
        "",
        home,
        name="home"
    ),

    # HemoBridge Admin Dashboard
    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),

    # Blood Request Management
    path(
        "dashboard/requests/",
        dashboard_requests,
        name="dashboard_requests"
    ),

    path(
        "dashboard/requests/<int:request_id>/approve/",
        approve_dashboard_request,
        name="approve_dashboard_request"
    ),

    path(
        "dashboard/requests/<int:request_id>/reject/",
        reject_dashboard_request,
        name="reject_dashboard_request"
    ),

    # Django Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # HemoBridge Applications
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
    path("hospitals/", include("hospitals.urls")),
]