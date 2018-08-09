import json, pprint, requests, textwrap
host = 'http://bigdata.ugr.es:5000/v3'
data = {'kind': 'spark'}
headers = {'Content-Type': 'application/json'}
r = requests.post(host + '/sessions', data=json.dumps(data), headers=headers)
r.json()

{u'state': u'starting', u'id': 0, u'kind': u'spark'}

session_url = host + r.headers['location']
r = requests.get(session_url, headers=headers)
r.json()

{u'state': u'idle', u'id': 0, u'kind': u'spark'}

