import os
import json


class EnvBackend(object):

    def load(self, key):
        return os.getenv(key)


class JsonFileBackend(object):

    def __init__(self, path):
        self._path = path

    def load(self, key):
        try:
            with open(self._path, 'r') as f:
                doc = json.load(f)

            return doc.get(key, None)
        except (IOError, ValueError):
            return None
