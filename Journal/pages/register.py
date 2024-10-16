import reflex as rx
from reflex.style import toggle_color_mode
from Journal.styles import auth_pages_stylesheet
from Journal.components.input_field import render_input_field
from Journal.states import State, RegisterState, Registration
from Journal.components.button import render_submit_button

@rx.page(route="/register")
def register() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.button(rx.icon("moon"), on_click=toggle_color_mode),
            width="100%",
            justify_content="end",
        ),
        rx.spacer(),
        rx.heading("Welcome to Journal!", size="8",
                   transition="all 550ms ease"),
        rx.text("Create an account to get started."),
        rx.divider(width="15%"),
        render_input_field(
            title="Username",
            is_password=False,
            value=RegisterState.username,
            update=RegisterState.update_username
            ),
        render_input_field(
            title="Email",
            is_password=False,
            value=RegisterState.email,
            update=RegisterState.update_email,
            ),
        render_input_field(
            title="Password",
            is_password=True,
            value=RegisterState.password,
            update=RegisterState.update_password,
            ),
        render_submit_button(
            name="Create Account!",
            event=Registration.user_registration
        ),
        *[rx.spacer() for _ in range(1)],
        rx.text(
            "Already have an account? Click ",
            rx.link("here", href="/"),
            "."
        ),
        rx.spacer(),
        style=auth_pages_stylesheet,
        spacing="2"
    )
