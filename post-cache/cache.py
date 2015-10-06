import requests
import sqlite3

class POSTCache:
    def __init__(self, cache_path, http_endpoint, async_interval=None, top_level_attributes={}):
        """
        Create a cache for POST requests.

        Args:
            cache_path: path to the sqlite3 database cached requests will be stored in
            http_endpoint: the url requests should be sent to. This endpoint should
                expect POST data with a "lines" attribute. "lines" will contain a list of the 
                individual request bodies that were cached.
            async_interval: If set, POSTCache will run a background thread to perform uploads
                every <interval> seconds. If not set, uploads will only be attempted when a new 
                request is added.
            top_level_attributes: A dictionary of key, value items to include in the top level
                POST data alongside "lines". 
        """
        self.cache_path = cache_path
        self.http_endpoint = http_endpoint
        self.async_interval = async_interval
        self.top_level_attributes = top_level_attributes

        self.cache_conn = sqlite3.connect(cache_path, check_same_thread=False)
        self.cache_c = self.cache_conn.cursor()
        self.cache_c.execute("CREATE TABLE if not exists postcache (request_body TEXT)")

    def add_request(self, body):
