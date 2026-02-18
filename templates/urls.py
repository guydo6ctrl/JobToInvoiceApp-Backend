from rest_framework.routers import DefaultRouter
from .views import ClientItemTemplateViewSet

router = DefaultRouter()
router.register(r"", ClientItemTemplateViewSet, basename="line-item-template")

urlpatterns = router.urls
