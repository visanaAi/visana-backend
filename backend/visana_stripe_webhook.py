from fastapi import FastAPI, Request
import stripe
import os

app = FastAPI()

# TEMP testing route
@app.get("/")
def read_root():
    return {"message": "Visana backend is live!"}

# Replace with your actual keys
stripe.api_key = "sk_test_your_key_here"
STRIPE_WEBHOOK_SECRET = "whsec_..."

@app.post("/stripe-webhook")
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

    if event['type'] == 'payment_intent.succeeded':
        print("✅ Payment succeeded!")

    return {"status": "success"}
