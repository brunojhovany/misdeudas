from functools import wraps
from flask import request
from jsonschema import validate
from models.json_schemas import Schemas

def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wraper(*args, **kw):
            try:
                schema = getattr(Schemas, schema_name)
                validate(request.json, schema=schema)
            except Exception as e:
                return {"error": e.message}, 400
            return f(*args, **kw)
        return wraper
    return decorator
