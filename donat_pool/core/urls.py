from .views import SiteSettingsViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'settings', SiteSettingsViewSet, basename='settings')

urlpatterns = router.urls

