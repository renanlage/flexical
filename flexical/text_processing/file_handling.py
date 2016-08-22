import io


def raw_read(filename, encoding):
    with io.open(filename, 'r', encoding=encoding) as _file:
        return _file.read()


def raw_write(filename, encoding, text):
    with io.open(filename, 'w', encoding=encoding) as _file:
        _file.write(text)


