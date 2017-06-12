class Peeker(object):
    """Class to support "peeking" into general iterables.

    IndexError is raised under two conditions:

        (1) The client peeks at an index greater than that of the last
            item in the iterable, and

        (2) The client advances to an index greater than the length of
            the iterable.

    Therefore, the client may advance to an index one greater than the
    greatest one at which it can peek.  This must be so, since the client
    must be allowed to advance by 0 when the iterable is empty, but the
    client must not be allowed to peek even at 0 in this case.

    """

    def __init__(self, iterable):
        """Initialize Peeker at start of iterable."""
        self._itr = iter(iterable)
        self._cache = []

    def __bool__(self):
        """Test whether Peeker has more values.

        Note that making this determination may require caching a
        value from the iterable.

        """
        self._cache.extend(self._itr)
        return bool(self._cache)

    def _read(self, n):
        """Return next n _itr values in iterable (IndexError on fail)."""
        if n == 0:
            return ()

        counter = 0
        for value in self._itr:
            yield value
            counter += 1
            if counter >= n:
                break
        else:
            raise IndexError('Index `{}` out of bounds.'.format(n))

    def peek(self, index):
        """Return value in iterable at index relative to window."""
        if index >= len(self._cache):
            self._cache.extend(self._read(index + 1 - len(self._cache)))
        return self._cache[index]

    def advance(self, steps):
        """Return current head and advance."""
        if steps >= len(self._cache):
            list(self._read(steps - len(self._cache)))
            self._cache = []
        else:
            self._cache = self._cache[steps:]
