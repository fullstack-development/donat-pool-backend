from .views import FundraisingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', FundraisingViewSet, basename='fundraising')

urlpatterns = router.urls
