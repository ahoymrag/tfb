# trust_fund_baby/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from datetime import datetime

app = FastAPI()

# Allow CORS (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- In-memory storage ----
users = {}
trust_goals = {}
deposits = {}
notes = {}

# ---- Pydantic models ----
class User(BaseModel):
    id: str
    email: str

class TrustGoal(BaseModel):
    id: str
    user_id: str
    name: str
    description: str = ""
    target_amount: float
    current_balance: float = 0.0
    created_at: datetime
    is_real: bool = False

class CreateTrustGoal(BaseModel):
    name: str
    description: str = ""
    target_amount: float

class Deposit(BaseModel):
    id: str
    trust_id: str
    amount: float
    timestamp: datetime

class Note(BaseModel):
    id: str
    trust_id: str
    content: str
    created_at: datetime

# ---- API routes ----

@app.post("/register", response_model=User)
def register_user(email: str):
    user_id = str(uuid4())
    user = User(id=user_id, email=email)
    users[user_id] = user
    return user

@app.post("/trusts", response_model=TrustGoal)
def create_trust(user_id: str, trust: CreateTrustGoal):
    trust_id = str(uuid4())
    new_trust = TrustGoal(
        id=trust_id,
        user_id=user_id,
        name=trust.name,
        description=trust.description,
        target_amount=trust.target_amount,
        created_at=datetime.utcnow()
    )
    trust_goals[trust_id] = new_trust
    return new_trust

@app.get("/trusts", response_model=List[TrustGoal])
def list_trusts(user_id: str):
    return [t for t in trust_goals.values() if t.user_id == user_id]

@app.get("/trusts/{trust_id}", response_model=TrustGoal)
def get_trust(trust_id: str):
    trust = trust_goals.get(trust_id)
    if not trust:
        raise HTTPException(status_code=404, detail="Trust not found")
    return trust

@app.post("/trusts/{trust_id}/deposit", response_model=Deposit)
def add_deposit(trust_id: str, amount: float):
    trust = trust_goals.get(trust_id)
    if not trust:
        raise HTTPException(status_code=404, detail="Trust not found")
    trust.current_balance += amount
    deposit_id = str(uuid4())
    deposit = Deposit(id=deposit_id, trust_id=trust_id, amount=amount, timestamp=datetime.utcnow())
    deposits[deposit_id] = deposit
    return deposit

@app.post("/trusts/{trust_id}/note", response_model=Note)
def add_note(trust_id: str, content: str):
    if trust_id not in trust_goals:
        raise HTTPException(status_code=404, detail="Trust not found")
    note_id = str(uuid4())
    note = Note(id=note_id, trust_id=trust_id, content=content, created_at=datetime.utcnow())
    notes[note_id] = note
    return note

@app.patch("/trusts/{trust_id}/make_real")
def mark_trust_real(trust_id: str):
    trust = trust_goals.get(trust_id)
    if not trust:
        raise HTTPException(status_code=404, detail="Trust not found")
    trust.is_real = True
    return {"message": "Trust marked as real."}

# ---- Project File Structure (MVP) ----
# trust_fund_baby/
# ├── main.py                # FastAPI app and routes (you’re here)
# ├── models.py              # (Optional) Split models out later
# ├── requirements.txt       # Dependencies
# ├── .env                   # Env variables (for Plaid keys later)
# ├── README.md              # Project overview and usage
# └── /static or /frontend   # Optional front-end POC (React or HTML)

# You can create requirements.txt with:
# fastapi
# uvicorn
# python-dotenv
# pydantic
