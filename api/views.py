from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.serializers import UserSerializer
from donations.models import Collect, Payment

User = get_user_model()


class UserViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CollectViewSet(ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = ...
