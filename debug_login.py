from app.database import SessionLocal
from app.models import User
from app.core.security import verify_password, get_password_hash

db = SessionLocal()
user = db.query(User).filter(User.email == "aeaa@neco.gov.ng").first()

if user:
    print(f"User exists. Email: {user.email}")
    print(f"Pass hash: {user.password}")
    print(f"Verify 'Admin@123': {verify_password('Admin@123', user.password)}")
else:
    print("User does not exist in the database! (Or email is not matching)")
