from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx

from app.database import get_db
from app.models.webhooks import Webhook
from app.models.events import Event
from app.schemas.events import EventCreate, EventResponse
from app.core.security import get_current_user

router = APIRouter(
    prefix="/webhooks",
    tags=["Events"]
)

@router.post(
    "/{webhook_id}/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED
)
def create_event(
    webhook_id: UUID,
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    webhook = (
        db.query(Webhook)
        .filter(
            Webhook.id == webhook_id,
            Webhook.user_id == current_user.id
        )
        .first()
    )

    if webhook is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )

    event = Event(
        webhook_id=webhook.id,
        event_type=event_data.event_type,
        payload=event_data.payload
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    delivery_payload = {
        "event_type": event.event_type,
        "payload": event.payload
    }

    response = httpx.post(
        webhook.url,
        json=delivery_payload,
        timeout=5.0
    )

    print("Webhook response status:", response.status_code)

    return event