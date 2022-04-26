"""Errors module."""


class QueryError(Exception):
    """Custom DB exception."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
