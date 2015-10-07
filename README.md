# python-post-cache
A Python library to cache data that is being POSTed to a remote server in the JSON format (such as periodic log items or measurements.

Requests with a JSON data body can be created using the add_request method. If an async_interval value was provided, these requests will be batched and POSTed to the server every `interval` seconds. If the upload fails they will be cached and resent at the next interval (along with any new data generated in the meantime).

If no async_interval is provided, uploads will be attempted synchronously when `add_request` is called. Failed POSTs will still be cached and uploaded next time `add_request` is called. 

Can be installed with `sudo pip install postcache`.

Basic usage can be found in the `examples/client.py` file:

```
cache = POSTCache("http://URL", "cache.db", async_interval=10)
cache.add_request(json.dumps({"timestamp": time.time(), "measurement":50}))
```