import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
import uuid
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.redis import RedisDep


class SecurityHandler:
    def __init__(self):
        self.pwd_context = PasswordHash.recommended()

        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def _create_token(self, data: dict, expires_delta: timedelta ,token_type: str) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire, "type": token_type})

        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def create_access_token(self, data: dict) -> str:
        return self._create_token(
            data=data,
            expires_delta=timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
            token_type="access"
        )

    def create_refresh_token(self, data: dict) -> tuple[str, str]:
        jti = str(uuid.uuid4())
        token = self._create_token(
            data={**data, "jti": jti},
            expires_delta=timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS),
            token_type="refresh"
        )
        return token, jti

    async def decode_token(self, token: str, jti: str, redis_client: RedisDep) -> dict:
        try:
            return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except ExpiredSignatureError:
            pass
        except InvalidTokenError:
            pass

security_handler = SecurityHandler()