import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token
from . import schemas
from .supabase_client import supabase

def get_user(data: schemas.Token):
    user = supabase.table("users").select("email").eq("token", data.access_token).single().execute()
    print(user)
    return user.email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/")

def get_current_user(data: str = Depends(oauth2_scheme)):
    print("Received token:", data) 
    print("Hi!..............................")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("hello.........")
    return token.verify_token(data, credentials_exception)

# def get_current_user():
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid Google token",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         return True
#     except:
#         raise credentials_exception

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid Google token",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         user_info = requests.get(
#             "https://www.googleapis.com/oauth2/v1/userinfo",
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         info = user_info.json()
#         email = info.get("email")
#         if not email:
#             raise credentials_exception
#         schemas.TokenData(email=email)
#         return user_info.json()
#     except:
#         raise credentials_exception