# coding: utf-8
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[int] = Field(None, primary_key=True, unique=True)
    username: str
    email: str
    is_deleted: bool = Field(default=False)
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        table = "users"


class Post(BaseModel):
    id: Optional[int] = Field(None, primary_key=True, unique=True)
    content: str
    user_id: int = Field(..., index=True)
    is_deleted: bool = Field(default=False)
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        table = "posts"
