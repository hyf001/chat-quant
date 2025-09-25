from typing import Optional
from pydantic import BaseModel,Field


class ChatRequest(BaseModel):
    user_content:str = Field(...,description="用户输入")
    thread_id:Optional[str] = Field("__default__",description="会话id")


class FeedbackRequest(BaseModel):
    feedback:str = Field(...,description="用户反馈")
    thread_id:Optional[str] = Field("__default__",description="会话id")
    