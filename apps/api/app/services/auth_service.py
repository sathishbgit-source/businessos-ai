from fastapi import HTTPException, status

from app.core.security.jwt import create_access_token
from app.core.security.password import hash_password, verify_password
from app.db.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(
        self,
        email: str,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> User:
        existing_user = await self.repository.get_by_email(email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            email=email,
            username=username,
            password_hash=hash_password(password),
            first_name=first_name,
            last_name=last_name,
        )

        return await self.repository.create(user)

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> str:
        user = await self.repository.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return create_access_token(str(user.id))

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)
