from typing import Optional

users = {}

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserService:
    @staticmethod
    def create_user(email: str, password: str) -> bool:
        if email in users:
            return False
        users[email] = User(email, password)
        print(users[email])
        return True


    # @staticmethod
    # def authenticate(email: str, password: str) -> Optional[User]:
    #     print("email",email,password)
    #     user = users.get(email)
    #     print("user",user)
    #     if user and user.password == password:
    #         return user
    #     return None
    @staticmethod
    def authenticate(email: str, password: str) -> Optional[dict]:
        print("email", email, password)
        print(users)
        user = users.get(email)
        print("user", user)
        if user and user.password == password:
            return user
        return None

