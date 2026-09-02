from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.models.webhooks import Webhook
from app.models.events import Event
from app.models.delivery_attempts import DeliveryAttempt

from app.api.user import router as users_router
from app.api.auth import router as auth_router
from app.api.webhooks import router as webhooks_router
from app.api.events import router as events_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Webhook Delivery Platform")
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(webhooks_router)
app.include_router(events_router)
@app.get("/")
def root():
    return {"message": "Webhook Platform is running"}