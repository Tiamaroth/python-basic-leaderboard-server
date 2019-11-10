class RequestError(Exception):
    """
        Generic error during a request. Contains a status_code and a bytes response.
    """
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message.encode("utf-8")