"""
URL configuration for donat_pool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from donat_pool.services.kupo.api import FundraisingInfoView
from donat_pool.services.moderation.api import ModerationView

urlpatterns = [
    path('core/', include('donat_pool.core.urls')),
    path('fundraisings/', include('donat_pool.fundraising.urls')),
    path('fundraising-api/<str:action>/', FundraisingInfoView.as_view(), name='fundraising_api'),
    path('moderation-api/<str:action>/', ModerationView.as_view(), name='moderation_api'),
    path('', admin.site.urls),
]
