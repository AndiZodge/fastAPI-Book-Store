from fastapi import  HTTPException, Request
from datetime import datetime, timedelta
from config import SECRET_KEY
import jwt
import logging
import sys



async def validate_token(request: Request):
    authorization = request.headers.get("authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        _, token = authorization.split("Bearer ")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")
    parse_token = await decode_jwt(token)

    return parse_token
    
    
def create_jwt(username, user_id, is_admin):
    payload = {
        "sub": user_id,
        "is_admin":is_admin,
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

async def decode_jwt(token: str):
    token = token.strip()
    try:
        return jwt.decode(token, options={"verify_signature": False, "verify_aud": False})
    except jwt.ExpiredSignatureError as jes:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as jit:
        raise HTTPException(status_code=401, detail="Invalid token")

async def check_admin_token(request):
    try:
        jwt_token = await validate_token(request)
        return jwt_token.get('is_admin', False)
    except Exception as ex:
        return False


def get_logger(logger_name=None, default_log_level=logging.DEBUG, module=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(default_log_level)
    logger.propagate = False
    if not module:
        module = 'Default'
    formatter = logging.Formatter("[%(levelname)s] :: %(asctime)s | %(lineno)s | {0} | %(message)s".format(module))
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    return logger