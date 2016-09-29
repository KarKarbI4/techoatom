class Charge:
    def __init__(self, value):
        self._value = value

    value = property()
    @value.getter
    def value(self):
        return round(self._value, 2)

    @value.setter
    def value(self, value):
        self._value = round(value, 2)

if __name__ == '__main__':
    charge = Charge(3.232324323)
    print(charge.value)