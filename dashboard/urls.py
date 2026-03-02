from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.dashboard_stats, name="dashboard-stats"),
    path("alerts/", views.dashboard_alerts, name="dashboard-alerts"),
]
