from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx

from app.database import get_db, SessionLocal

from app.models.webhooks import Webhook
from app.models.events import Event
from app.models.delivery_attempts import DeliveryAttempt

from app.schemas.events import EventCreate, EventResponse
from app.core.security import get_current_user

router = APIRouter(
    prefix="/webhooks",
    tags=["Events"]
)

def deliver_event(event_id: UUID,webhook_url: str, event_type: str, payload: dict):

    db = SessionLocal()

    try:
        attempt = DeliveryAttempt(
            event_id=event_id,
            attempt_number=1,
            status="PENDING"
        )

        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        delivery_payload = {
            "event_type": event_type,
            "payload": payload
        }

        try:
            response = httpx.post(
                webhook_url,
                json=delivery_payload,
                timeout=5.0
            )

            attempt.response_status_code = response.status_code

            if 200 <= response.status_code < 300:
                attempt.status = "SUCCESS"
            else:
                attempt.status = "FAILED"

        except httpx.HTTPError as exc:
            attempt.status = "FAILED"
            attempt.error_message = str(exc)

        db.commit()

        if attempt.status == "SUCCESS":
            print("Webhook response status:", attempt.response_status_code)
        else:
            print("Webhook delivery failed:", attempt.error_message)

    finally:
        db.close()

@router.post(
    "/{webhook_id}/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED
)
def create_event(
    webhook_id: UUID,
    event_data: EventCreate,
    background_tasks: BackgroundTasks,
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

    background_tasks.add_task(
        deliver_event,
        event.id,
        str(webhook.url),
        event.event_type,
        event.payload
    )

    return event