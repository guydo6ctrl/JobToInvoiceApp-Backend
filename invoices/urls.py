from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, invoice_download_view

router = DefaultRouter()
router.register(r"", InvoiceViewSet, basename="invoice")

urlpatterns = [
    # This is the extra function-based view
    path("<int:invoice_id>/download/", invoice_download_view, name="invoice-download"),
    # Include the router’s ViewSet URLs
    path("", include(router.urls)),
]
