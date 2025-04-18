from django.contrib.auth import get_user_model
from rest_framework import serializers

from donations.models import Collect, Payment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        pw = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(pw)
        user.save()
        return user


class CollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = (
            'owner',
            'title',
            'reason',
            'description',
            'goal_value',
            'image',
            'finish_at'
        )
