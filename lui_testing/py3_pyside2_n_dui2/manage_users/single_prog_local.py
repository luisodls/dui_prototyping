import hashlib
import secrets
import getpass
from datetime import datetime

class SimpleAuthSystem:
    def __init__(self):
        self.users = {}  # username -> user_data
        self.tokens = {}  # token -> username

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_token(self):
        return secrets.token_hex(16)

    def create_user(self, username, password):
        if username in self.users:
            return False, "Username already exists"

        password_hash = self.hash_password(password)
        self.users[username] = {
            'password_hash': password_hash,
            'created_at': datetime.now()
        }
        return True, "User created successfully"

    def login(self, username, password):
        if username not in self.users:
            return False, "User does not exist"

        password_hash = self.hash_password(password)
        if self.users[username]['password_hash'] != password_hash:
            return False, "Invalid password"

        token = self.generate_token()
        self.tokens[token] = username
        return True, token

    def validate_token(self, token):
        return self.tokens.get(token)

    def logout(self, token):
        if token in self.tokens:
            del self.tokens[token]
            return True, "Logged out successfully"
        return False, "Invalid token"

    def list_users(self):
        return list(self.users.keys())

    def list_tokens(self):
        return self.tokens.copy()

def main():
    auth = SimpleAuthSystem()

    print("=== Simple Authentication System ===")
    print("Commands: register, login, validate, logout, users, tokens, quit")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == 'register':
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")

            success, message = auth.create_user(username, password)
            print(f"Result: {message}")

        elif command == 'login':
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")

            success, message = auth.login(username, password)
            if success:
                print(f"Login successful! Your token: {message}")
            else:
                print(f"Login failed: {message}")

        elif command == 'validate':
            token = input("Token: ").strip()
            username = auth.validate_token(token)

            if username:
                print(f"Token valid! User: {username}")
            else:
                print("Invalid token")

        elif command == 'logout':
            token = input("Token: ").strip()
            success, message = auth.logout(token)
            print(f"Result: {message}")

        elif command == 'users':
            users = auth.list_users()
            print(f"Registered users: {users}")

        elif command == 'tokens':
            tokens = auth.list_tokens()
            print("Active tokens:")
            for token, username in tokens.items():
                print(f"  {username}: {token[:16]}...")

        elif command in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        else:
            print("Unknown command. Available: register, login, validate, logout, users, tokens, quit")

if __name__ == "__main__":
    main()
