from fastapi import FastAPI, Request
import stripe
import os

app = FastAPI()

# Replace this with your real Stripe secret
stripe.api_key = "sk_test_your_key_here"

# Stripe webhook secret (optional but recommended for security)
STRIPE_WEBHOOK_SECRET = "whsec_..."

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return {"error": "Invalid signature"}
    except Exception as e:
        return {"error": str(e)}

    # Example: handle successful payment
    if event['type'] == 'payment_intent.succeeded':
        print("✅ Payment succeeded!")

    return {"status": "success"}
from fastapi import Request

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    return {"status": "Webhook received!"}
