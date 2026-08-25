from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class EventCreate(BaseModel):
    event_type: str
    payload: dict


class EventResponse(BaseModel):
    id: UUID
    webhook_id: UUID
    event_type: str
    payload: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)