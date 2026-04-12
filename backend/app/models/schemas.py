from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import Optional, List, Any, Annotated
from datetime import datetime
from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a string in the API (JSON) 
# and be stored as an ObjectId in MongoDB.
def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[str | ObjectId, BeforeValidator(validate_object_id)]

class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
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
