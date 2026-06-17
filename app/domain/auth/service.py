import secrets
from app.core.config import settings
from app.core.security import security_handler
from app.domain.user.models import User, UserRole
from app.domain.user.repository import UserRepository
from app.infrastructure.github.oauth import GitHubOAuth


class AuthService:

    def __init__(self, user_repo: UserRepository, github: GitHubOAuth, redis):
        self.user_repo = user_repo
        self.github = github
        self.redis = redis

    async def create_authorize_urls(self) -> str:
        state = secrets.token_urlsafe(32)
        await self.redis.setex(f"oauth_state:{state}", settings.STATE_TTL, "1")
        return self.github.build_authorize_url(state=state)


    async def handle_callback(self, code: str, state: str) -> tuple[str, str]:
        if not await self.redis.get(f"oauth_state:{state}"):
            pass # 에러 헨들러 만들면 채움
        await self.redis.delete(f"oauth_state:{state}")

        github_token = await self.github.exchange_code(code)
        github_user = await self.github.fetch_user(github_token)

        user = await self.user_repo.get_user_by_github_id(github_user['id'])
        if user is None:
            user = await self.user_repo.create(User(
                github_id=github_user['id'],
                username=github_user['login'],
                avatar_url=github_user['avatar_url'],
                role=UserRole.MEMBER,
            ))
        return await self._issue_tokens(user)


    async def refresh(self, refresh_token: str | None) -> tuple[str, str]:
        if not refresh_token:
            pass # 에러 헨들러 만들면 채움
        payload = await security_handler.decode_token(refresh_token)
        if payload is None or payload.get('type') != 'refresh':
            pass # 에러 헨들러 만들면 채움

        jti = payload.get('jti')
        if not await self.redis.get(f"refresh_jti:{jti}"):
            pass  # 에러 헨들러 만들면 채움
        await self.redis.delete(f"refresh_jti:{jti}")

        user = await self.user_repo.get_user_by_github_id(int(payload['sub']))
        if not user:
            pass # 에러 헨들러 만들면 채움
        return await self._issue_tokens(user)


    async def logout(self, refresh_token: str | None) -> None:
        if not refresh_token:
            pass  # 에러 헨들러 만들면 채움
        payload = await security_handler.decode_token(refresh_token)
        if payload and payload.get("type") == "refresh":
            await self.redis.delete(f"refresh_jti:{payload['jti']}")


    async def _issue_tokens(self, user: User) -> tuple[str, str]:
        access = security_handler.create_access_token(
            {"sub": str(user.id), "role": user.role.value}
        )
        refresh, jti = security_handler.create_refresh_token({"sub": str(user.id)})
        ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        await self.redis.setex(f"refresh_jti:{jti}", ttl, str(user.id))
        return access, refresh