from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from finance.models import Account


class AccountSerializer(serializers.ModelSerializer):
    number = serializers.CharField(
        max_length=22,
        validators=[
            UniqueNumberValidator(queryset=Account.objects.all())
        ])

    class Meta:
        model = Account
        fields = ['number', 'amount']


class UniqueNumberValidator(object):

    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, value):
        if self.queryset.filter(number=value).exists():
            raise serializers.ValidationError('This field must be a unique.')
