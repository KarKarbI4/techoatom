from decimal import Decimal
from datetime import date


class Charge:

    def __init__(self, value, _date):
        self.check(value, _date)
        self._value = round(Decimal(value), 2)
        self._date = _date

    @staticmethod
    def check(value, _date):
        if value < 0 and _date > date.today():
            raise ValueError('Charge off are not supported for future')

    @property
    def value(self):
        return self._value

    @property
    def date(self):
        return self._date

    def __repr__(self):
        return 'Charge(Value: {0}, Date: {1})'.format(self.value, self.date)

if __name__ == '__main__':
    ch = Charge(3.12345, date.today())
    print(ch)
