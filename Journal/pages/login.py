import reflex as rx
from reflex.style import toggle_color_mode
from Journal.styles import auth_pages_stylesheet
from Journal.components.input_field import render_input_field
from Journal.states import State, LoginState, Authentication
from Journal.components.button import render_submit_button
from ..templates import template
from ..components.profile_input import profile_input

# @rx.page(route="/login")
# def login() -> rx.Component:
#     return rx.vstack(
#         # rx.hstack(
#         #     rx.button(rx.icon("moon"), on_click=toggle_color_mode),
#         #     width="100%",
#         #     justify_content="end",
#         # ),
#         rx.spacer(),
#         rx.heading("Welcome Back!", size="8",
#                    transition="all 550ms ease"),
#         rx.text("Sign in below to access your account."),
#         rx.divider(width="15%"),
#         render_input_field(
#             title="Email",
#             is_password=False,
#             value=LoginState.email,
#             update=LoginState.update_email,
#             ),
#         render_input_field(
#             title="Password",
#             is_password=True,
#             value=LoginState.password,
#             update=LoginState.update_password,
#             ),
#         render_submit_button(
#             name="Login!",
#             event=Authentication.user_login,
#         ),
#         *[rx.spacer() for _ in range(2)],
#         rx.text(
#             "Don't have an account? Click ",
#             rx.link("here", href="/register"),
#             "."
#         ),
#         rx.spacer(),
#         style=auth_pages_stylesheet,
#         spacing="2"
#     )

#TODO: Center components
# Profile page, when not logged in
@template(route="/login", title="Login")
def login() -> rx.Component:
    """The profile page to login.

    Returns:
        The UI for the login page.
    """
    return rx.vstack(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon("square-user-round"),
                    rx.heading("Login", size="5"),
                    align="center",
                ),
                rx.text("User your email and password to login.", size="3"),
                width="100%",
                position="center"
            ),
            rx.form.root(
                rx.vstack(
                    profile_input(
                        label="User Email",
                        name="email",
                        placeholder="Email",
                        type="text",
                        icon="user",
                        default_value="",
                    ),
                    profile_input(
                        label="Password",
                        name="password",
                        placeholder="password",
                        type="password",
                        icon="mail",
                        default_value="",
                    ),
                    rx.button("Login", type="submit", width="100%"),
                    width="100%",
                    spacing="5",
                ),
                on_submit=Authentication.handle_submit,
                # on_submit=lambda form_data: rx.window_alert(form_data.to_string()),
                reset_on_submit=True,
                width="100%",
                max_width="325px",
            ),
            rx.spacer(),
            *[rx.spacer() for _ in range(2)],
            rx.text(
                "Don't have an account? ",
                rx.link("Bet", href="/register"),"!"
            ),
            width="100%",
            spacing="4",
            flex_direction=["column", "column", "row"],
            justify_content="center",

        ),
        rx.divider(),
        spacing="6",
        width="100%",
        max_width="800px",
    )
