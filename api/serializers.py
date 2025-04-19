from django.contrib.auth import get_user_model
from django.utils import timezone as tz
from rest_framework import serializers

from api.fields import Base64ImageField
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


class PaymentSerializer(serializers.ModelSerializer):
    payer = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'total',
            'payment_date',
            'payer'
        )


class CollectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    participants = serializers.IntegerField(default=0, read_only=True)
    collected = serializers.IntegerField(default=0, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Collect
        fields = (
            'owner',
            'title',
            'reason',
            'description',
            'goal_value',
            'collected',
            'participants',
            'image',
            'created_at',
            'finish_at',
            'payments'
        )

    def validate_finish_at(self, value):
        if value < tz.now():
            raise serializers.ValidationError(
                'Нельзя устанавливать дату в прошлом!'
            )
        return value

    def create(self, validated_data):
        collect = Collect.objects.create(
            **validated_data,
            owner=self.context['request'].user
        )
        return collect
