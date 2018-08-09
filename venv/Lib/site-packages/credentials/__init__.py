import os

from .base import Credentials
from .backends import EnvBackend, JsonFileBackend

active_backends = [
    EnvBackend(),
    JsonFileBackend(os.path.expanduser('~/.credentials.json'))
]
credentials = Credentials(active_backends)
