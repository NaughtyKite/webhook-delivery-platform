from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.webhooks import Webhook
from app.schemas.webhooks import WebhookCreate, WebhookResponse
from app.core.security import get_current_user


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)


@router.post(
    "/",
    response_model=WebhookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_webhook(
    webhook_data: WebhookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    webhook = Webhook(
        user_id=current_user.id,
        url=str(webhook_data.url)
    )

    db.add(webhook)
    db.commit()
    db.refresh(webhook)

    return webhook

@router.get(
    "/",
    response_model=list[WebhookResponse]
)
def get_webhooks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    webhooks = (
        db.query(Webhook)
        .filter(Webhook.user_id == current_user.id)
        .all()
    )

    return webhooks

@router.get(
    "/{webhook_id}",
    response_model=WebhookResponse
)
def get_webhook(
    webhook_id: UUID,
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

    return webhook

@router.delete("/{webhook_id}")
def delete_webhook(
    webhook_id: UUID,
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

    db.delete(webhook)
    db.commit()

    return {
        "message": "Webhook deleted successfully"
    }