import pydantic
from typing import Any, Dict, Type


class BaseModel(pydantic.BaseModel):
    
    class Config:
        populate_by_name = True
        loc_by_alias = False

        # from https://github.com/tiangolo/fastapi/issues/1810#issuecomment-895126406
        @staticmethod
        def json_schema_extra(schema: Dict[str, Any], model: Type['BaseModel']) -> None:
            snake_case = {}
            for field in model.__fields__.values():
                k = field.name
                v = schema['properties'][field.alias]
                snake_case.update({k: v})
            schema.update({'properties': snake_case})
