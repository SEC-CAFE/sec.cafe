from typing import List, Dict, Union
import orjson
from pydantic import BaseModel


class Response(BaseModel):
    code: int = 0
    data: Union[List, Dict] = list()
    message: str = 'success'


class ResponseModel(BaseModel):
    code: int = 0
    data: Dict = dict()
    message: str = 'success'


# orjson https://pydantic-docs.helpmanual.io/usage/exporting_models/
# https://yanbin.blog/python-json-choose-ujson-if-necessary/
class CustomModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


# https://fastapi.tiangolo.com/tutorial/handling-errors/
class CustomException(Exception):
    def __init__(self, code: int, message: str, data: Union[List, Dict] = []):
        self.response = Response(code=code, message=message, data=data)
