import reflex as rx
import pandas as pd
from .models import CustomPost, StatsMetrics
from .api import get_post_stats_endpoint, get_posts_with_comments_api, insert_comment_to_database, insert_post_to_database, user_login_endpoint, user_logout_endpoint, user_registration_endpoint, is_user_authenticated, get_usernames

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

    async def user_logout(self):
        response = await user_logout_endpoint(self.access_token)

        # perform any pre-logout clean up: ie clear cookies...
        self.access_token = ""

        if response == 204:
            return rx.redirect("/")

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
                # print(f"in notebook landing --> {self.posts}")
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

class Comments(Authentication):
    post_comment: str = ""#object that handles user's comment...

    async def void_event(self):...

    async def update_post_comment(self, post_comment):
        self.post_comment = post_comment

    # method that changes comment visibility on event
    async def set_comment_visibility_to_flex(self, post: dict):
        post["is_comment_visible"] = (
            "flex" if post["is_comment_visible"] == "none" else
            "none"
        )
        #add a return statement
        return post

    # method to update comment form visibility...
    def update_posts_with_comment_visibility(self, post_with_comment: dict):
        for post in self.posts:
            if post.id == post_with_comment["id"]:
                post.is_comment_visible = post_with_comment["is_comment_visible"]
            else:
                post.is_comment_visible = "none"
        self.post_comment = ""

    # toggle method for the comment
    async def toggle_comment(self, post):
        _post: dict = await self.set_comment_visibility_to_flex(post)
        self.update_posts_with_comment_visibility(_post)

#TODO: PostDATA
    async def commit_comment_to_post(self, post: CustomPost):
        data = {
            "user_id": self.user_id,
            "post_id": post["id"],
            "content": self.post_comment
        }

        res = await insert_comment_to_database(
            access_token=self.access_token,
            comment=data
        )

        await self.toggle_comment(post)

        if res == 201:
            self.posts = await get_posts_with_comments_api(
                self.access_token, self.username_list
            )
            return rx.redirect("/notebook")

class Post(Authentication):
    post_intention: str
    post_success: str
    post_lesson: str
    post_grateful: str
    post_lesson_score: int = 0
    post_success_score: int = 0


    is_open: bool = False

    async def clear_post_entries(self):
        self.post_intention, self.post_success = "", ""
        self.post_lesson, self.post_grateful = "", ""
        self.post_lesson_score, self.post_success_score = 0, 0

    def toggle_post_form(self):
        self.is_open = not (self.is_open)

    def update_post_intention(self, post_intention):
        self.post_intention = post_intention

    def update_post_success(self, post_success):
        self.post_success = post_success

    def update_post_lesson(self, post_lesson):
        self.post_lesson = post_lesson

    def update_post_grateful(self, post_grateful):
        self.post_grateful = post_grateful

    def update_post_lesson_score(self, post_lesson_score):
        self.post_lesson_score = post_lesson_score[0]

    def update_post_success_score(self, post_success_score):
        self.post_success_score = post_success_score[0]


    # method to insert post to supabase DB
    async def submit_post_for_validation(self):
        #make any pre-validation checks here
        if await is_user_authenticated(self.access_token) is True:
            response = await insert_post_to_database(
                access_token=self.access_token,
                user_id=self.user_id,
                post_intention=self.post_intention,
                post_success=self.post_success,
                post_lesson=self.post_lesson,
                post_grateful=self.post_grateful,
                post_lesson_score=self.post_lesson_score,
                post_success_score=self.post_success_score,
            )

            if response == 200 or response == 201:
                self.toggle_post_form()

                # update post data
                self.posts = await get_posts_with_comments_api(
                    access_token=self.access_token,
                    username_list=self.username_list
                )

                await self.clear_post_entries()

                return rx.redirect("/notebook")
        else:
            print("Acess token not valid.")

class Stats(Authentication):
    """
    Method that handles on Stats page landing, ie when user
    reaches the /stats page
    """
    # x: list[str]
    # y: list[int]
    posts_stats: list[StatsMetrics]


    async def on_stats_landing_event(self):
        if not self.access_token:
            self.posts_stats = []
            return rx.redirect(path="/")
        else:
            if await self.is_access_token_valid() is True:
                await self.get_posts_stats()
                # await self.set_x_df()
                # await self.set_y_df()
                # print(f"in stats landing --> {self.posts}")

            else:
                return rx.redirect(path="/")

    # if the user does have an access token, check if user is validated/authenticated
    async def is_access_token_valid(self):
        if await is_user_authenticated(self.access_token) is True:
            return True
        else:
            return False

    # if the token is valid, we need to get the post and fill up the list...
    async def get_posts_stats(self):
        self.posts_stats = await get_post_stats_endpoint(
            self.access_token, self.user_id
        )

    # async def set_x_df(self):
    #     self.x = await get_x_df(
    #         self.access_token, self.posts
    #     )
    # async def set_y_df(self):
    #     self.y = await get_stats_df_endpoint(
    #         self.access_token, self.posts
    #     )

class Profile(Authentication):
    """
    Class for the profile page where user has users' information along with
        drainers and gainers, and goals defined.
    """
    ...
