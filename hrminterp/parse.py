import io


def parse_program(source_stream):
    parser = Parser(source_stream)
    return parser.parse()


class ParseResult(object):
    def __init__(self):
        self.labels = {}
        self.instructions = []


class Parser(object):
    def __init__(self, stream):
        self._stream = stream
        self._line = 1
        self._program = ParseResult()
        self._offset = 0
        stream.seek(0, io.SEEK_END)
        self._stream_end = stream.tell()
        stream.seek(0, io.SEEK_SET)

    def parse(self):
        self._read_line()  # skip human resource machine program line
        while not self._eof():
            line = self._read_line().strip().split()
            if len(line) == 0:
                continue
            if line[0] == "DEFINE":
                data = self._read_until(";")
            elif line[0].endswith(":"):
                label_name = line[0][:-1]
                self._program.labels[label_name] = self._offset
            elif line[0].lower() != "comment":
                self._program.instructions.append(line)
                self._offset += 1
        return self._program

    def _eof(self):
        return self._stream.tell() >= self._stream_end

    def _read_line(self):
        if not self._eof():
            line = self._stream.readline()
            self._line += 1
        else:
            line = None
        return line

    def _read_until(self, delimiter):
        buffer = ""
        while not self._eof():
            got = self._stream.read(1)
            if got != delimiter:
                buffer += got
            else:
                break
        if self._eof():
            buffer = None
        return buffer
