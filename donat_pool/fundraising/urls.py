from .views import FundraisingViewSet, CompletedFundraisingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', FundraisingViewSet, basename='fundraising')
router.register(r'archive', CompletedFundraisingViewSet, basename='archive')

urlpatterns = router.urls
