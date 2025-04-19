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
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, data):
        if (
                data['email'] == ''
                or data['first_name'] == ''
                or data['last_name'] == ''
        ):
            raise serializers.ValidationError('Заполните все данные!')

        return data

    def create(self, validated_data):
        pw = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(pw)
        user.save()
        return user


class CollectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Collect
        fields = (
            'owner',
            'title',
            'reason',
            'description',
            'goal_value',
            'current_value',
            'image',
            'created_at',
            'finish_at'
        )
        read_only_fields = (
            'current_value',
            'created_at'
        )

    def create(self, validated_data):
        owner = self.context['request'].user
        collect = Collect.objects.create(
            **validated_data,
            owner=owner
        )
        owner.email_user(
            subject=f'{validated_data["title"]} состоится!',
            message=f'{owner.get_full_name()} сбор средств начался!',
        )
        return collect

