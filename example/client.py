#!/usr/bin/python
from postCache import POSTCache
import json, time

cache = POSTCache("http://localhost:8080/tracking/api/gps", "cache.db", async_interval=10)

cache.add_request(json.dumps({"date": "now", "latitude":35}))
time.sleep(20)