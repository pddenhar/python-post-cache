#!/usr/bin/python
from postcache import POSTCache
import json, time

#synchronous use of postcache
cache = POSTCache("http://localhost:8080/tracking/api/gps", "cache.db")
cache.add_request(json.dumps({"date": "now", "latitude":35}))
time.sleep(2)

#asynchronous use of postcache
cache = POSTCache("http://localhost:8080/tracking/api/gps", "cache.db", async_interval=10)
cache.add_request(json.dumps({"date": "now", "latitude":35}))
cache.add_request(json.dumps({"date": "now", "latitude":36}))
cache.add_request(json.dumps({"date": "now", "latitude":37}))
cache.add_request(json.dumps({"date": "now", "latitude":38}))
time.sleep(15)