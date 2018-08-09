[![Build Status](https://travis-ci.org/OniOni/credentials.svg?branch=master)](https://travis-ci.org/OniOni/credentials)

# Installing
```shell
$ pip install credentials
```

# Usage

## Default
Using default setup, this will try and load credentials first from the processes environement variables and then from `~/.credentials.json`
```python
from credentials import credentials
# load credentials up front
creds = credentials.require(['cred1', 'cred2'])
function_that_needs_creds(creds.cred1)
...
# load credentials as needed
my_cred = credentials.load('cred_3')
function_that_needs_creds(my_cred)
...
```

## Setting up your own loader
```python
# Only load credentias from environement
from credentials import Credentials, EnvBackend
creds = Credentials([EnvBackend()])
...
```

# Implementing your own backend
A backend is just an object with a `load` method. Method should take a `key` as an argument and return the associated credentials or `None` if it could not be loaded.

Example:
```python
class UniversalCredLoader(object):

   def load(self, key):
      return 42
...
from credentials import Credentials
creds = Credentials([UniversalCredLoader()])
cred.load('cred1')
>>> 42
```


