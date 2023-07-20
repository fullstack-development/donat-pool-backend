from .views import FundraisingViewSet, CompletedFundraisingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'archive', CompletedFundraisingViewSet, basename='archive')
router.register(r'', FundraisingViewSet, basename='fundraising')

urlpatterns = router.urls
