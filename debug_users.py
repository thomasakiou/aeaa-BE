from app.database import SessionLocal
from app.models import User
import sys

try:
    db = SessionLocal()
    users = db.query(User).all()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"User: {u.email} | Role: {u.role}")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
