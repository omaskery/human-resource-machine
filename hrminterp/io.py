from .value import Value


class InputDevice(object):
    def read(self):
        return None


class OutputDevice(object):
    def write(self, value):
        pass


class FileInput(InputDevice):
    def __init__(self, file):
        self._values = list(map(
            Value.parse,
            file.read().split(",")
        ))

    def read(self):
        if len(self._values) > 0:
            next = self._values[0]
            self._values = self._values[1:]
            return next
        else:
            return None


class ConsoleInput(InputDevice):
    def read(self):
        value = Value.parse(input("input> "))
        return value


class FileOutput(OutputDevice):
    def __init__(self, file):
        self._file = file
        self._first = True

    def write(self, value):
        if not self._first:
            self._file.write(",")
            self._first = True
        self._file.write(str(value))


class ConsoleOutput(OutputDevice):
    def write(self, value):
        print("output> {}".format(value))

