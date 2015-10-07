import requests, json, threading
import sqlite3, time

class POSTCache:
    def __init__(self, http_endpoint, cache_path, async_interval=None, top_level_attributes={}, upload_limit=500):
        """
        Create a cache for POST requests.

        Args:
            http_endpoint: the url requests should be sent to. This endpoint should
                expect POST data with a "lines" attribute. "lines" will contain a list of the 
                individual request bodies that were cached.
            cache_path: path to the sqlite3 database cached requests will be stored in
            async_interval: If set, POSTCache will run a background thread to perform uploads
                every <interval> seconds. If not set, uploads will only be attempted when a new 
                request is added.
            top_level_attributes: A dictionary of key, value items to include in the top level
                POST data alongside "lines". 
            upload_limit: If cached requests are available, how many to upload per interval
        """
        self.cache_path = cache_path
        self.http_endpoint = http_endpoint
        self.async_interval = async_interval
        self.top_level_attributes = top_level_attributes
        self.upload_limit = upload_limit

        self.cache_conn = sqlite3.connect(cache_path)
        self.cache_c = self.cache_conn.cursor()
        self.cache_c.execute("CREATE TABLE if not exists postcache (request_body TEXT)")

        self.offloader = POSTCache.OffloadService(self)
        if self.async_interval != None:
            self.offloader.start()
    def add_request(self, body):
        """
        Add a new request to the stack of requests to be sent to the server
        If async_interval is not set, this request (and any cached ones) 
        will go out right away. If it is set, this request will be batched
        and sent out after <interval>

        Args:
            body: JSON string to be included as the data in the post request
        """
        self.cache_c.execute("INSERT into postcache VALUES (?)", [body])
        self.cache_conn.commit()
        if self.async_interval == None:
            self.offloader.flush_cache()

    class OffloadService(threading.Thread):
        def __init__(self, post_cache):
            threading.Thread.__init__(self)
            self.post_cache = post_cache
            #use the parent object's cache cursor, will get replaced with a different one 
            #if run is called
            self.cache_c = self.post_cache.cache_c
            self.cache_conn = self.post_cache.cache_conn

            self.running = True
            self.parent = threading.current_thread()
        def flush_cache(self):
            limit = self.post_cache.upload_limit
            self.cache_c.execute("select ROWID, request_body from postcache ORDER BY ROWID ASC limit {0}".format(limit))
            rows = self.cache_c.fetchall()
            if(len(rows) > 0):
                max_row_id = rows[-1][0]
                payload = {}
                payload.update(self.post_cache.top_level_attributes)
                payload["lines"] = [json.loads(row[1]) for row in rows]
                try:
                    r = requests.post(self.post_cache.http_endpoint, json = payload)
                    self.cache_c.execute("delete from postcache where ROWID <= ?", [max_row_id])
                    self.cache_conn.commit()
                    if r.status_code != 200:
                        raise Exception("A server error occured({0}): {1}".format(r.status_code, r.text))
                except Exception as e:
                    print e
        def run(self):
            self.cache_conn = sqlite3.connect(self.post_cache.cache_path)
            self.cache_c = self.cache_conn.cursor()
            while self.running:
                self.flush_cache()
                for i in range(self.post_cache.async_interval * 10):
                    if not (self.running and self.parent.is_alive()) : return
                    time.sleep(.1)