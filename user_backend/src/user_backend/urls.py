"""
URL configuration for user_backend project.

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
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers

from user_backend import settings
from users.views import UserViewSet, PatientToDocktorViewSet, PatientToDocktorListViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"doctors/(?P<doctor_pk>\d+)", PatientToDocktorListViewSet)
router.register(r"doctors/(?P<doctor_pk>\d+)/users", PatientToDocktorViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls))
]

# если не на production:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))