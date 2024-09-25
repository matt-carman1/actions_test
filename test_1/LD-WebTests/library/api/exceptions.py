class LiveDesignAPIException(Exception):
    """
    Exception thrown by the core API test framework
    """

    def __init__(self, msg, error=None):
        self.msg = msg
        self.error = error

    def __str__(self):
        return repr(self.msg)
