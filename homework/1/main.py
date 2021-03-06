class Charge:
    def __init__(self, value):
        self._value = round(float(value), 2)

    value = property()
    @value.getter
    def value(self):
        return round(self._value, 2)

    def __str__(self):
        return str(self.value)

class Account:
    def __init__(self, total=0):
        self._charges = []
        self._total = round(float(total), 2)

    @property
    def charges(self):
        return self._charges

    @property
    def total(self):
        return round(self._total, 2)

    def __iter__(self):
        return iter(self.charges)

    def transaction(self, charge):
        self._charges.append(charge)
        self._total = max(self._total + charge.value, 0)

    def __str__(self):
        return 'Account Charges: {0}\nCurrent Balance: {1}'.format(', '.join(map(str, self.charges)), self.total)

if __name__ == '__main__':
    charge1 = Charge(3)
    charge2 = Charge(9.3235)
    charge3 = Charge(-4)
    # charge4 = Charge(-94.0333)
    print(charge1)
    account = Account()
    account.transaction(charge1)
    account.transaction(charge2)
    account.transaction(charge3)
    # account.transaction(charge4)
    print(account)
    for charge in account:
        print(charge)