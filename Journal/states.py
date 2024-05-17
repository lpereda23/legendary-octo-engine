import reflex as rx

class State(rx.State):
    def void_event(self): ...

class LoginState(State):
    email: str
    password: str

    def update_email(self, email):
        self.email = email

    def update_password(self, password):
        self.password = password

class RegisterState(State):
    username: str
    email: str
    password: str

    def update_username(self, username):
        self.username = username

    def update_email(self, email):
        self.email = email

    def update_password(self, password):
        self.password = password
