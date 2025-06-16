from passlib.context import CryptContext


pwd = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd.hash(password)

def verify_password(plain: str,hashed):
    #get hashed?
    return pwd.verify(plain, hashed)

