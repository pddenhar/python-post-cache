python-post-cache
=================
A Python library to cache data that is being POSTed to a remote server in the JSON format (such as periodic log items or measurements. Probably most useful in situations where data needs to be logged from devices with lossy connections, or where power may be lost before transmission. 

Requests with a JSON data body can be created using the `add_request method`. If an `async_interval` value was provided, these requests will be batched and POSTed to the server every `interval` seconds. If the upload fails they will be cached and resent at the next interval (along with any new data generated in the meantime).

If no `async_interval` is provided, uploads will be attempted synchronously when `add_request` is called. Failed POSTs will still be cached and uploaded next time `add_request` is called. 

HTTP Endpoints
--------------
Your HTTP endpoint should expect a POST request with JSON data included. Flask's `get_json()` is an example of an easy way to access it. The JSON will be structured as follows:
```
{
  lines: [
    request1_body,
    request2_body
  ],
  top_level_attribute1: "value1",
  top_level_attribute2: 22
}
```
Lines is the set of cached request JSON bodies that were uploaded for the current interval. In the general case there might just be one item in it.

Top level attributes are extra pieces of data you want to include that are not specific to one request, such as device IP or hostname. They are added when instantiating POSTCache using `top_level_attributes`.

Installation
------------
Can be installed with `sudo pip install postcache`.

Basic usage can be found in the `examples/client.py` file:

```
from postcache import POSTCache
import time

cache = POSTCache("http://URL", "cache.db", async_interval=10)
for i in range(0,20):
  cache.add_request(json.dumps({"timestamp": time.time(), "measurement":i * 2}))
```
