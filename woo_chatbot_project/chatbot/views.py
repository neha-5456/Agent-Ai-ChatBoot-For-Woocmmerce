import requests
import os
import openai
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

WC_API_URL = os.getenv("WC_API_URL")  # e.g. https://yourstore.com/wp-json/wc/v3/
WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def wc_get(endpoint, params=None):
    """Helper to call WooCommerce API"""
    r = requests.get(
        WC_API_URL + endpoint,
        auth=(WC_CONSUMER_KEY, WC_CONSUMER_SECRET),
        params=params,
    )
    return r.json()

@api_view(["POST"])
@permission_classes([AllowAny])
def chatbot_reply(request):
    data = request.data
    intent = data.get("intent", "other")
    query = data.get("query", "")

    # --- Handle Intents ---
    if intent == "check_order":
        orders = wc_get("orders", {"search": query})
        if orders:
            order = orders[0]
            reply = f"Order {order['id']} is currently {order['status']} and total {order['total']}."
        else:
            reply = "Sorry, I could not find an order with that ID/email."
        return Response({"reply": reply})

    elif intent == "browse_products":
        products = wc_get("products", {"per_page": 5})
        reply = "Here are some products:\n" + "\n".join(
            [f"{p['name']} - ${p['price']} → {p['permalink']}" for p in products]
        )
        return Response({"reply": reply})

    elif intent == "get_discount":
        reply = "🎟️ Use coupon code DEMO10 for 10% off your next order."
        return Response({"reply": reply})

    # --- Fallback to AI ---
    if OPENAI_API_KEY:
        prompt = f"You are a WooCommerce shopping assistant. Customer asked: {query}"
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful shopping assistant for WooCommerce."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
        )
        reply = completion.choices[0].message["content"]
        return Response({"reply": reply})

    return Response({"reply": "AI not configured."})
