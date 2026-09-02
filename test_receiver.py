from fastapi import FastAPI
import asyncio

app = FastAPI(title="Webhook Test Receiver")


@app.post("/webhook")
async def receive_webhook(payload: dict):
    await asyncio.sleep(1)
    print("----- WEBHOOK RECEIVED -----")
    print(payload)
    print("----------------------------")

    return {
        "status": "received"
    }