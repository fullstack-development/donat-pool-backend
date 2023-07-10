from .views import SiteSettingsViewSet, FeedbackViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'settings', SiteSettingsViewSet, basename='settings')
router.register(r'contact-us', FeedbackViewSet, basename='contact-us')
urlpatterns = router.urls
