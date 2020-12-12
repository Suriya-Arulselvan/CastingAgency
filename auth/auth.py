import os
from jose import jwt
from flask import request
from urllib.request import urlopen
import json
from functools import wraps

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN").replace("\r", "")
ALGORITHMS = os.getenv("ALGORITHMS").replace("\r", "")
API_AUDIENCE = os.getenv("API_AUDIENCE").replace("\r", "")

"""
AuthError Exception 
A standardized way to communicate auth failure modes
"""


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


"""
Get_Token_Auth_Header
- gets the header from the request
- raises AuthError if no header present
- Attempt to split bearer and token
- raises AuthError if header is malformed
- return token part of the header
"""


def get_token_auth_header():
    if "Authorization" not in request.headers:
        raise AuthError({"code": "unauthorized", "message": "No Authorization header"}, 401)

    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(" ")

    if len(header_parts) != 2:
        AuthError({"code": "unauthorized", "message": "No Authorization header"}, 401)
    elif header_parts[0].lower() == "bearer":
        AuthError({"code": "unauthorized", "message": "Not bearer token"}, 401)

    return header_parts[1]


"""
Check_permissions
- inputs: 
    1. permission: string permission (i.e., "post:movie")
    2. payload: decoded jwt payload
- raises AuthError if permissions not included in the payload
- raises AuthError if requested permission string is not in the payload permission array
- return true otherwise
"""


def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError({"code": "invalid_claims", "message": "Permissions not included in JWT"}, 400)

    if permission not in payload["permissions"]:
        raise AuthError({"code": "unauthorized", "message": "Permission not found"}, 403)

    return True


"""
Verify_decode_jwt
- input: a json web token (string)
- verify that the input should be an Auth0 token with kid
- verify the token using Auth0 /.well-known/jwks.json
- decode the payload from the token
- validate the claims
- return decoded payload
"""


def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError({"code": "invalid_header", "message": "Authorization malformed"}, 401)

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}

    if rsa_key:
        try:
            payload = jwt.decode(
                token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer="https://" + AUTH0_DOMAIN + "/"
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired", "message": "Token expired"}, 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                {"code": "invalid_claims", "message": "Incorrect claims. Please, check the audience and issuer."},
                401,
            )

        except Exception:
            raise AuthError({"code": "invalid_header", "message": "Unable to parse authentication token"}, 400)
    raise AuthError({"code": "invalid_header", "message": "Unable to find the appropriate key."}, 400)


"""
@requires_auth(permission)
- Input: permission (string. eg. "post:movie")
- call the get_token_auth_header method to get the token
- call verify_decode_jwt method to decode the jwt
- call check_permissions method to validate claims and check requested permission
- return decorator which passes the decoded payload to the decorated method
"""


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
