from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from finance.models import Account, Charge, User
from finance.validators import ValidateCharacters, ValidateLuhnChecksum, ValidateNotAZero, StripToNumbers


class UniqueNumberValidator(object):
    
    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, value):
        if self.queryset.filter(number=value).exists():
            raise serializers.ValidationError('This field must be a unique.')


class CardNumberValidator():

    def __call__(self, number):
        """ Check that a credit card number matches the type and validates the Luhn Checksum """
        if not ValidateCharacters(number):
            raise serializers.ValidationError(
                'Can only contain numbers and spaces.')
        number = StripToNumbers(number)
        if not ValidateNotAZero(number):
            raise serializers.ValidationError('Can not be zeros')
        if not ValidateLuhnChecksum(number):
            raise serializers.ValidationError(
                'Not a valid credit card number.')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'address']


class AccountSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    card_num = serializers.CharField(
        max_length=16,
        validators=[
            UniqueNumberValidator(queryset=Account.objects.all()),
            CardNumberValidator,
        ])

    class Meta:
        model = Account
        fields = ['id', 'name', 'card_num', 'total', 'owner']


class ChargeSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Charge
        fields = [
            'id',
            'account',
            'value',
            'date'
        ]
        read_only_fields = [
            'id',
        ]


