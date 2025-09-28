from app import app  # Import the main app instance

from ..models.user import User
from ..services.user_service import UserService

user_service = UserService() # Initialize the service

@app.get("/users")
def get_users():
    return user_service.get_all_users()

@app.post("/users")
def create_user(user: User):
    return user_service.create_user(user)
