from fastapi import HTTPException, status
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone

TOKEN_SECRET = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lcnMiOlsiZmFjdSJdLCJpYXQiOjE3MTc3NTkwMDd9.IS-b1sl51lAO5MKAN4ci6u0ehbmJ-nKWz-UM_FrMSp0"
TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRATION_TIME = 2

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes = TOKEN_EXPIRATION_TIME)

    to_encode.update({ "exp": expire })

    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET, algorithm=TOKEN_ALGORITHM)

    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, TOKEN_SECRET, algorithms = [TOKEN_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")