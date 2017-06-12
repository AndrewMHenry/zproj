class Sequencer(object):
    """Object that implements sequence protocol on general iterable."""

    def __init__(self, itr):
        """Initialize Sequencer on iterable itr."""
        self._itr = itr
        self._cache = []

    def __iter__(self):
        yield from self._cache
        yield from self._itr

    def _update(self, index):
        if index >= len(self._cache):
            self._cache.extend(next(self._itr)
                               for i in range(index - len(self._cache)))

    def _capitulate(self):
        """Give up and cache the entire iterable."""
        self._cache.extend(self._itr)

    def __getitem__(self, index):
        """Return item at index."""
        self._update(index)
        return self._cache[index]

    def __setitem__(self, index, value):
        """Item at index = value."""
        self._update(index)
        self._cache[index] = value

    def __len__(self):
        """Return length of entire iterable."""
        self._capitulate()
        return len(self._cache)

    def 
