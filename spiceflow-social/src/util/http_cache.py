# Placeholder for future ETag/Last-Modified caching interface.
# Implement later when SPICEFLOW_ALLOW_RUN=1.
class HTTPCache:
    def preflight(self, url:str)->dict:  # returns headers to send
        return {}
    def store(self, url:str, response):  # record etag/last-modified
        pass
