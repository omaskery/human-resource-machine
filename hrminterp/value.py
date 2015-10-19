import string


class Value(object):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @staticmethod
    def parse(value):
        value = value.strip()
        if all([c in string.digits for c in value]):
            return Value(int(value))
        elif len(value) == 1:
            return Value(value)
        else:
            raise Exception("unable to convert {} to value".format(value))

    def is_text(self):
        return isinstance(self._value, str)

    def __add__(self, other):
        if self.is_text() != other.is_text():
            raise Exception("tried to add a character and an integer: {} and {}".format(self.value, other.value))
        if self.is_text() and other.is_text():
            return Value(ord(self.value) + ord(other.value))
        else:
            return Value(self.value + other.value)

    def __sub__(self, other):
        if self.is_text() != other.is_text():
            raise Exception("tried to sub a character and an integer: {} and {}".format(self.value, other.value))
        if self.is_text() and other.is_text():
            return Value(ord(self.value) - ord(other.value))
        else:
            return Value(self.value - other.value)

