from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.api.user import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Webhook Delivery Platform")
app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Webhook Platform is running"}