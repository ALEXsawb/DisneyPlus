from typing import List, Union, Optional

from bson import ObjectId
from passlib.context import CryptContext
from pydantic import AnyHttpUrl, EmailStr
from pymongo.results import UpdateResult

from backend.models.IdFIeld import IdField
from backend.schemas.User import AuthUserAccount, User
from backend.schemas.Visit import Visit
from backend.StarWars.services.decorations import invalid_update
from backend.db.db import users

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(IdField, AuthUserAccount):
    visits: Union[list, List[AnyHttpUrl]]

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PWD_CONTEXT.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return PWD_CONTEXT.hash(password)

    async def save(self):
        self.password = self.get_password_hash(self.password)
        user = await users.insert_one(self.dict())
        self.id = user.inserted_id
        return user

    @classmethod
    async def verified(cls, email: EmailStr, password: str) -> dict:
        user = await users.find_one({'email': email}, {'_id': 1, 'email': 1, 'password': 1})
        if not user or not cls.verify_password(hashed_password=user['password'], plain_password=password):
            raise ValueError('Incorrect Email or Password')
        return user

    @classmethod
    async def get_users(cls, users_limit: Optional[int] = 10, visits_limit: Optional[int] = 10,
                        skip: Optional[int] = 0) -> List[dict]:
        users_ = users.find({}, {'_id': 1,
                                 'email': 1,
                                 'visits': {'$slice': [-visits_limit, visits_limit]},
                                 'visits_count': {'$size': '$visits'}}
                            ).skip(skip).to_list(users_limit)
        users_ = await users_
        return [User.parse_obj(user).dict() for user in users_]

    @classmethod
    async def get_visits(cls, user_id: str, limit: Optional[int] = 10, skip: Optional[int] = 0) -> dict:
        return await users.find_one({'_id': ObjectId(user_id)},
                                    {'_id': 0, 'email': 0, 'password': 0, 'admin': 0,
                                     'visits': {'$slice': [-(skip + limit), limit]}},)

    @classmethod
    async def get_documents_count(cls) -> int:
        return await users.count_documents({})

    @classmethod
    @invalid_update
    async def add_visit(cls, visit: Visit) -> UpdateResult:
        return await users.update_one({'_id': ObjectId(visit.end_user_id)},
                                      {'$push': {'visits': visit.web_page_url}})

    def dict(self, *args, **kwargs) -> dict:
        kwargs['exclude_unset'] = True
        kwargs['exclude_none'] = True
        return super().dict(*args, **kwargs)
