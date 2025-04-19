from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CollectViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('collects', CollectViewSet, basename='collect')

urlpatterns = [
    path('', include(router.urls))
]
