import reflex as rx
from .models import CustomPost
from .api import get_posts_with_comments_api, user_login_endpoint, user_registration_endpoint, is_user_authenticated, get_usernames

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

class Registration(RegisterState):
    async def user_registration(self):
        if (
            await user_registration_endpoint(
                username=self.username, email=self.email, password=self.password
            )
            is True
        ):
            print("User registration OK.")
            return rx.redirect("/")
        else:
            print("User reg. NOT OK.")

class Authentication(LoginState):
    access_token: str
    user_id: str
    user_email: str
    session_exp: str

    user_cookies: str = rx.Cookie(name="Journal")

    posts: list[CustomPost] # pass the data model here...
    username_list: list [dict]

    async def user_cookie(self):
        self.user_cookies = {
            "user_id": self.user_id,
            "user_email": self.user_email,
            "expires_in": self.session_exp
        }

    async def get_username_list(self):
        self.username_list = await get_usernames()

    async def user_login(self):
        (
            self.access_token,
            self.session_exp,
            self.user_id,
            self.user_email,
        ) = await user_login_endpoint(
            self.email,
            self.password
        )

        await self.user_cookie()

        await self.get_username_list()
        return rx.redirect("/notebook")

class JournalData(Authentication):
    """
    Method that handles on Journal landing, ie when user reaches the /notebook route
    """
    async def on_notebook_landing_event(self):
        if not self.access_token:
            self.posts = []
            return rx.redirect(path="/")
        else:
            if await self.is_access_token_valid() is True:
                await self.get_posts_with_comments()
                print(f"in notebook landing --> {self.posts}")
            else:
                return rx.redirect(path="/")

    # if the user does have an access token, check if user is validated/authenticated
    async def is_access_token_valid(self):
        if await is_user_authenticated(self.access_token) is True:
            return True
        else:
            return False

    # if the token is valid, we need to get the post and fill up the list...
    async def get_posts_with_comments(self):
        self.posts = await get_posts_with_comments_api(
            self.access_token, self.username_list
        )
        # print(self.posts)
