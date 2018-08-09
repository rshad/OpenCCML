from collections import namedtuple


class Credentials(object):

    def __init__(self, backends):
        self._backends = backends

    def add_backend(self, backend):
        self._backends.append(backend)

    def load(self, key):
        values = [x for x in [b.load(key) for b in self._backends]
                  if x is not None]

        if len(values) > 0:
            return values[0]

        raise KeyError("Could not load '%s'" % key)

    def require(self, required):
        Credential = namedtuple('Credential', required)
        return Credential(**{k: self.load(k) for k in required})
