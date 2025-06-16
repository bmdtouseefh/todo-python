from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRET_KEY="sahdfjsdaifjsd12fsdjcdsjfij142jkljvdfu90"
ALGO="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
    return encoded_jwt
