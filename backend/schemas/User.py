from typing import Optional

from pydantic import BaseModel, EmailStr, Field, AnyHttpUrl

from backend.models.IdFIeld import IdField


class AuthUserAccount(BaseModel):
    email: EmailStr
    password: str
    admin: Optional[bool]


class User(IdField, BaseModel):
    email: EmailStr
    visits: list[AnyHttpUrl]
    visits_count: int = Field(ge=0, default=0)

    def dict(self, *args, **kwargs) -> dict:
        dict_ = super().dict(*args, **kwargs)
        dict_['id'] = str(dict_['id'])
        return dict_
