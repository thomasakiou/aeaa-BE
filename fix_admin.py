from app.database import SessionLocal
from app.models import User, RoleEnum
from app.core.security import get_password_hash

db = SessionLocal()
emails = ["aeaa@neco.gov.ng", "aeaa2027@neco.gov.ng"]

for email in emails:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        new_admin = User(
            fullName="System Administrator",
            email=email,
            password=get_password_hash("Admin@123"),
            role=RoleEnum.ADMIN
        )
        db.add(new_admin)
        print(f"Created {email}")
    else:
        user.password = get_password_hash("Admin@123")
        print(f"Updated password for {email}")

db.commit()
db.close()
