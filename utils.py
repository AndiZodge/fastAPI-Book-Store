from fastapi import  HTTPException, Request
from datetime import datetime, timedelta
from config import SECRET_KEY
import jwt
import logging
import sys



async def validate_token(request: Request):
    try:
        authorization = request.headers.get("authorization")
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        _, token = authorization.split("Bearer ")
        return await decode_jwt(token)

    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid token format") from e

    

# TODO: timeout should be customizable from config
def create_jwt(user_data: dict) -> str:
    payload = {
        "sub": user_data.user_id,
        "is_admin": user_data.is_admin,
        "username": user_data.username,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


async def decode_jwt(token: str) -> dict:
    token = token.strip()
    try:
        return jwt.decode(token, options={"verify_signature": False, "verify_aud": False})
    except jwt.ExpiredSignatureError as jes:
        raise HTTPException(status_code=401, detail=str(jes))
    except jwt.InvalidTokenError as jit:
        raise HTTPException(status_code=401, detail=str(jit))

async def check_admin_token(request) -> bool:
    try:
        jwt_token = await validate_token(request)
        return jwt_token.get('is_admin', False)
    except Exception as ex: # CHECK: using base level exception
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