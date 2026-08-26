from fastapi import FastAPI

app = FastAPI(title="Webhook Test Receiver")


@app.post("/webhook")
async def receive_webhook(payload: dict):
    print("----- WEBHOOK RECEIVED -----")
    print(payload)
    print("----------------------------")

    return {
        "status": "received"
    }