from django.contrib import admin
from django.urls import path, include
from users.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("clients/", include("clients.urls")),
    path("jobs/", include("jobs.urls")),
    path("invoices/", include("invoices.urls")),
    path("quotes/", include("quotes.urls")),
]
