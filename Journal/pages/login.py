import reflex as rx
from reflex.style import toggle_color_mode
from Journal.styles import auth_pages_stylesheet
from Journal.components.input_field import render_input_field
from Journal.states import State, LoginState, Authentication
from Journal.components.button import render_submit_button

@rx.page(route="/")
def login() -> rx.Component:
    return rx.vstack(
        # rx.hstack(
        #     rx.button(rx.icon("moon"), on_click=toggle_color_mode),
        #     width="100%",
        #     justify_content="end",
        # ),
        rx.spacer(),
        rx.heading("Welcome Back!", size="8",
                   transition="all 550ms ease"),
        rx.text("Sign in below to access your account."),
        rx.divider(width="15%"),
        render_input_field(
            title="Email",
            is_password=False,
            value=LoginState.email,
            update=LoginState.update_email,
            ),
        render_input_field(
            title="Password",
            is_password=True,
            value=LoginState.password,
            update=LoginState.update_password,
            ),
        render_submit_button(
            name="Login!",
            event=Authentication.user_login
        ),
        *[rx.spacer() for _ in range(2)],
        rx.text(
            "Don't have an account? Click ",
            rx.link("here", href="/register"),
            "."
        ),
        rx.spacer(),
        style=auth_pages_stylesheet,
        spacing="2"
    )
