from typing import Any

def to_camel_case(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def dict_to_camel_case(obj: dict) -> dict:
    return {to_camel_case(k): v for k, v in obj.items()} if isinstance(obj, dict) else obj

def get_pagination(skip: int = 0, limit: int = 100):
    return skip, limit
