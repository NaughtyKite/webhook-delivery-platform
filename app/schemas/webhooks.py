from pydantic import BaseModel, HttpUrl, ConfigDict
from uuid import UUID
from datetime import datetime


class WebhookCreate(BaseModel):
    url: HttpUrl


class WebhookResponse(BaseModel):
    id: UUID
    user_id: int
    url: str
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)