# 🍼 Trust Fund Baby

Trust Fund Baby is a calm and visual legacy tracker that helps users simulate “trust goals” — like a kid’s college fund, creative savings, or a future self project — and turn them into real legal trust funds later.

## 🚀 MVP Features

- Create “Trust Goals”
- Simulate manual deposits
- Add notes to each goal
- Track savings progress
- Mark a goal as “real” to upgrade later

## 🧰 Tech Stack

- FastAPI
- SQLite (in-memory for now)
- Python 3.10+
- Uvicorn
- Pydantic

## 🛠 Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
