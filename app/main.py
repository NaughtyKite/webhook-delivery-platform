from fastapi import FastAPI

app = FastAPI(title="Webhook Delivery Platform")


@app.get("/")
def root():
    return {"message": "Webhook Platform is running"}