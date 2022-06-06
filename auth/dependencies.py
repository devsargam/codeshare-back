from codeshare.settings import get_crypto_context
from fastapi.param_functions import Depends
from .models import User
from fastapi import status, HTTPException
import os
from .schema import PydanticUser
from datetime import datetime, timedelta
from jose import JWTError, jwt
from codeshare.settings import get_crypto_context, get_oauth_2_scheme


async def add_user(user: PydanticUser) -> User:

    if len(user.password) < 8:
        raise HTTPException(
            detail="enter a password of length greater than 8",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if len(user.password) > 80:
        raise HTTPException(
            detail="password too long",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if await User.get_or_none(username=user.username):
        raise HTTPException(
            detail="username already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    password = get_crypto_context().hash(user.password)
    created_user = await User.create(username=user.username, password=password)
    if user.is_admin:
        created_user.is_admin = True
        await created_user.save()
    return created_user


async def authenticate_user(username: str, password: str):
    if user := await User.get_or_none(username=username):
        if not get_crypto_context().verify(password, user.password):
            return False
        return user


async def create_token(user):
    to_encode = dict(user)
    del to_encode["password"]

    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=os.environ.get(
            "ALGORITHM")
    )
    return encoded_jwt


async def get_user_from_token(token: str = Depends(get_oauth_2_scheme())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if user := await User.get(username=username):
        return user
    else:
        raise credentials_exception


async def get_super_user(user: PydanticUser):
    if user.is_admin:
        return user
    else:
        return None


async def get_user(user: PydanticUser = Depends(get_user_from_token)):
    return user
