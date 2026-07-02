from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from collections import defaultdict

app = FastAPI()

# CORS for browser grader
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_u3n61r8yiuov0chww31w1tl9"
EMAIL = "24f3002540@ds.study.iitm.ac.in"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.get("/")
def home():
    return {"message": "Analytics API running"}


@app.post("/analytics")
def analytics(
    data: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key")
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = data.events

    total_events = len(events)
    unique_users = len(set(event.user for event in events))

    revenue = 0.0
    positive_totals = defaultdict(float)

    for event in events:
        if event.amount > 0:
            revenue += event.amount
            positive_totals[event.user] += event.amount

    if positive_totals:
        top_user = max(positive_totals, key=positive_totals.get)
    else:
        top_user = ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }