from rest_framework.routers import DefaultRouter
from .views import BankDetailsViewSet, CompanyDetailsViewSet

router = DefaultRouter()
router.register(r"details", CompanyDetailsViewSet, basename="details")
router.register(r"bank", BankDetailsViewSet, basename="bank")

urlpatterns = router.urls
