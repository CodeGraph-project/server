from pydantic import BaseModel


class AuthorizeUrlResponse(BaseModel):
    authorize_url: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"