class Charge:
    def __init__(self, value):
        self._value = round(float(value), 2)

    value = property()
    @value.getter
    def value(self):
        return round(self._value, 2)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

class Account:

    def __init__(self):
        self._charges = []
        self._total = 0

    @property
    def charges(self):
        return self._charges

    @property
    def total(self):
        return self._total

    def __iter__(self):
        return iter(self.charges)

    def transaction(self, charge):
        self._charges.append(charge)
        self._total += charge.value

    def __str__(self):
        return 'Account Charges:{0}\nCurrent Balance:{1}'.format(self.charges, self.total)

    def __repr__(self):
        return str(self)

if __name__ == '__main__':
    charge1 = Charge(3)
    charge2 = Charge(3.232324323)
    print(charge1.value)

    account = Account()
    account.transaction(charge1)
    account.transaction(charge2)
    print(account)