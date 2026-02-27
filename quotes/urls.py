from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet, quote_download_view

router = DefaultRouter()
router.register(r"", QuoteViewSet, basename="quote")

urlpatterns = [
    # This is the extra function-based view
    path("<int:quote_id>/download/", quote_download_view, name="quote-download"),
    # Include the router’s ViewSet URLs
    path("", include(router.urls)),
]
