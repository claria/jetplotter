def auto(iterable):
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
    while saved:
        yield saved[-1]
