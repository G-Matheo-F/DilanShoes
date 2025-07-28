from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import os
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "esta-es-una-clave-secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # solo para esquema

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user_if_needed(db: Session):
    if not db.query(User).filter_by(username="admin").first():
        hashed_password = get_password_hash("admin123")
        user = User(username="admin", hashed_password=hashed_password)
        db.add(user)
        db.commit()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception()
        return username
    except JWTError:
        raise credentials_exception()

def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = None):
    username = decode_access_token(token)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception()
    return user

# Extra para sacar token directo de la cookie sin usar OAuth2PasswordBearer (para templates)

from fastapi import Cookie

def get_token_from_cookie(access_token: str | None = Cookie(default=None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="No autenticado (cookie)")
    return access_token
