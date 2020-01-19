from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

def requiered_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 1 not in claims['roles']:
            return "requiered admin", 401
        # if user is not logged in, redirect to login page

        return f(*args, **kwargs)

    return wrap
