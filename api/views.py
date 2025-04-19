from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CollectSerializer, PaymentSerializer,
                             UserSerializer)
from donations.models import Collect, Payment

User = get_user_model()


class UserViewSet(CreateModelMixin, ListModelMixin,
                  RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CollectViewSet(ModelViewSet):
    serializer_class = CollectSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Collect.objects.annotate(participants=Count('payments'),
                                        collected=Sum('payments__total'))


class PaymentViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_collect(self):
        return get_object_or_404(
            Collect,
            pk=self.kwargs.get('collect_id')
        )

    def get_queryset(self):
        return self.get_collect().payments.all()

    def perform_create(self, serializer):
        serializer.save(collect=self.get_collect(), payer=self.request.user)
