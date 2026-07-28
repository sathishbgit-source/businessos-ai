from fastapi import HTTPException, status

from app.core.security.jwt import create_access_token
from app.core.security.password import hash_password, verify_password
from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(
        self,
        request: RegisterRequest,
    ) -> User:
        existing_user = await self.repository.get_by_email(request.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            email=request.email,
            username=request.username,
            password_hash=hash_password(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
        )

        return await self.repository.create(user)

    async def authenticate_user(
        self,
        request: LoginRequest,
    ) -> TokenResponse:
        user = await self.repository.get_by_email(request.email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            token_type="bearer",
        )

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)
