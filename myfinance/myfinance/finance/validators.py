import re
from django.core.exceptions import ValidationError

def ValidateLuhnChecksum(number_as_string):
    """ checks to make sure that the card passes a luhn mod-10 checksum """

    sum = 0
    num_digits = len(number_as_string)
    oddeven = num_digits & 1

    for i in range(0, num_digits):
        digit = int(number_as_string[i])

        if not ((i & 1) ^ oddeven):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum = sum + digit

    return ((sum % 10) == 0)


def ValidateCharacters(number):
    """ Checks to make sure string only contains valid characters """
    return re.compile('^[0-9 ]*$').match(number) != None


def StripToNumbers(number):
    """ remove spaces from the number """
    if ValidateCharacters(number):
        result = ''
        rx = re.compile('^[0-9]$')
        for d in number:
            if rx.match(d):
                result += d
        return result
    else:
        raise ValueError('Number has invalid digits')

def ValidateNotAZero(number):
    return int(number) != 0

def ValidateCreditCard(number):
    """ Check that a credit card number matches the type and validates the Luhn Checksum """
    if not ValidateCharacters(number):
        raise ValidationError('Can only contain numbers and spaces.')
    number = StripToNumbers(number)
    if not ValidateNotAZero(number):
        raise ValidationError('Can not be zeros')
    if not ValidateLuhnChecksum(number):
        raise ValidationError('Not a valid credit card number.')
