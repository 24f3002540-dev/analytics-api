from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from collections import defaultdict

app = FastAPI()

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
    x_api_key: Optional[str] = Header(default=None)
):
    if x_api_key != API_KEY:
        return JSONResponse(status_code=401, content={"valid": False})

    events = data.events

    total_events = len(events)
    unique_users = len(set(e.user for e in events))

    revenue = 0.0
    user_totals = defaultdict(float)

    for e in events:
        if e.amount > 0:
            revenue += e.amount
            user_totals[e.user] += e.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }