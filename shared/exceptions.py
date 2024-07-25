from fastapi import Request
from fastapi.responses import JSONResponse

class NotFound(Exception):
    def __init__(self, name: str):
        self.name = name