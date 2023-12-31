from bson import ObjectId
from pydantic import BaseModel, Field


class IdFieldConfiguration(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class IdField(IdFieldConfiguration, BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")