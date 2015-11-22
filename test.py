import redis
from itertools import imap
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set("shweta", "katheria")
b = r.get("shweta")
r.set("yo",15215)
print abs(-454)
print r.get("yo")
print b