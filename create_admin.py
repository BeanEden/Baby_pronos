from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        username = "admin admin"
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(
                username=username,
                password_hash=generate_password_hash("123", method="pbkdf2:sha256"),
                is_admin=True,
                category="Famille"
            )
            db.session.add(user)
            print("Admin account created.")
        else:
            user.password_hash = generate_password_hash("123", method="pbkdf2:sha256")
            user.is_admin = True
            print("Admin account updated.")
        db.session.commit()

if __name__ == "__main__":
    create_admin()
