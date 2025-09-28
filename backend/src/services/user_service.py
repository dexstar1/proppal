from typing import List, Optional

from ..models.user import User


class UserService:
    def __init__(self):
        self.users = [
            User(
                id=1, name="Admin User",
                email="admin@example.com",
                password_hash="hashed_password",
                role="Admin"
            ),
            User(
                id=2, name="Realtor User",
                email="realtor@example.com",
                password_hash="hashed_password",
                role="Realtor"
            ),
        ]

    def get_all_users(self) -> List[User]:
        return self.users

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return next((user for user in self.users if user.id == user_id), None)

    def create_user(self, user: User) -> User:
        user.id = len(self.users) + 1
        self.users.append(user)
        return user

    def update_user(self, user_id: int, updated_user: User) -> Optional[User]:
        for i, user in enumerate(self.users):
            if user.id == user_id:
                self.users[i] = updated_user
                self.users[i].id = user_id # Ensure ID remains the same
                return self.users[i]
        return None

    def delete_user(self, user_id: int) -> bool:
        initial_len = len(self.users)
        self.users = [user for user in self.users if user.id != user_id]
        return len(self.users) < initial_len
