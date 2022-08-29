from pydantic import BaseModel as pydanticBase, Extra


class BaseModel(pydanticBase):
    class Config:
        extra = Extra.forbid
