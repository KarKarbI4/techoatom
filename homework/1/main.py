class Charge:
    def __init__(self, value):
        self._value = float(value)

    value = property()
    @value.getter
    def value(self):
        return round(self._value, 2)

if __name__ == '__main__':
    charge = Charge(3)
    charge = Charge(3.232324323)
    print(charge.value)