from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

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

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase, MongoBaseModel):
    hashed_password: str
    streak: int = 0
    last_active: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserPublic(UserBase):
    streak: int
    last_active: Optional[datetime]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class TaskBase(BaseModel):
    task_en: str
    task_hi: str
    date: str  # YYYY-MM-DD

class TaskInDB(TaskBase, MongoBaseModel):
    pass

class sessionBase(BaseModel):
    user_input: str
    corrected_text: str
    hindi_explanation: str
    feedback: str
    score: int
    date: datetime = Field(default_factory=datetime.utcnow)

class sessionInDB(sessionBase, MongoBaseModel):
    user_id: PyObjectId
