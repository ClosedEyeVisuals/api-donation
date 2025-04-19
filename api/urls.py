from django.conf import settings
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views import CollectViewSet, PaymentViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('collects', CollectViewSet, basename='collect')
router.register(
    r'collects/(?P<collect_id>\d+)/payments',
    PaymentViewSet,
    basename='payment'
)

urlpatterns = [
    path('', include(router.urls))
]

schema_view = get_schema_view(
    openapi.Info(
      title="Donation Service API",
      default_version='v1',
      description="Документанция к API сервиса по сбору денежных средств."
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns += [
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    )
]
