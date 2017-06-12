class Reader(object):

    def __init__(self, itr):
        self._itr = itr
        self._cache = []
        self._base = 0

    def peek(self, index):
        if len(self._cache) <= index:
            try:
                self._cache.extend(next(self._itr) for i in range(index
            except StopIteration:
                raise SyntaxError('Index `{}` out of bounds.'.format(index))
        return self._cache[self._base + index]

    def advance(self, step):
        self._base += step
