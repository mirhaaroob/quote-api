from fastapi import FastAPI, Request
from pydantic import BaseModel
import random
from datetime import datetime

app = FastAPI(title="Quote of the Day API")

quotes = [
    {"id": 1, "text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"id": 2, "text": "Simplicity is the soul of efficiency.", "author": "Austin Freeman"},
    {"id": 3, "text": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House"},
]

webhook_log = []


class QuoteIn(BaseModel):
    text: str
    author: str


@app.get("/")
def root():
    return {"message": "Quote of the Day API is running", "endpoints": ["/quote", "/quotes", "/webhook"]}


@app.get("/quote")
def get_random_quote():
    quote = random.choice(quotes)
    return quote


@app.post("/quotes")
def add_quote(quote: QuoteIn):
    new_id = max(q["id"] for q in quotes) + 1
    new_quote = {"id": new_id, "text": quote.text, "author": quote.author}
    quotes.append(new_quote)
    return {"message": "Quote added", "quote": new_quote}


@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    entry = {"received_at": datetime.utcnow().isoformat(), "payload": payload}
    webhook_log.append(entry)
    return {"status": "received", "logged_entries": len(webhook_log)}


@app.get("/webhook/log")
def get_webhook_log():
    return {"count": len(webhook_log), "entries": webhook_log}
