import reflex as rx
from Journal.states import Authentication, LoginState, State


# class ProfileState(rx.State):
gainers = ["Music", "Nature", "Cuddling a/your pet", "Grounding(bare feet walk)", "Eating clean healthy nutrition",
            "Good night sleep", "Offline time", "Quality time with a (positive) good friend", "Meditate",
            "Breathwork", "Just sit still (and stare at nature/the clouds/the grass)", "Breathwork",
            "Workout", "Stretch", "Go to Spa", "Go on a week(end) trip", "Journal your thoughts",
            "Write down your dreams and visualize them", "Read", "Learn something new (a course / seminar / youtube)",
            "Dance (like no one's watching)", "Have sex", "Take a nap",
            "Saying no (so you say even more YESSS to what is really important to you)",
            "Add+"]
drainers = ["Being around synic / negative / complaining / harsh / dominating people",
        "Saying yes to everything and everyone", "No time management", "Reactive behavior",
        "Not being reliable to your own word with respect to others BUT EVEN MORE TOWARDS YOUR OWN WORD",
            "Going to bed too late", "Sleeping inconsistent", "Not having enough hours of sleep (i.e. < 7,5 hours)",
            "Eating processed foods // rich of sugar // rich of saturated fats", "Sitting still whole day",
            "Being inside the whole day",
            "Doom scrolling and other dopamine kick habits (and out of a sudden don't have enough time to work on your goals anymore...)",
            "Procrastination of important tasks", "Snoozing", "Warm long morning showers during working days",
            "Having calories within 2 hours before sleep", "Not having a morning AND evening routine",
            " Dehydration (< 2L of water)", "Drinking > 4 cups of coffee",
            "Drinking alcohol (Short run: affects your sleep quality, sharpness, energy, mood; Long run affects your quality of life, health and perception of your mood",
            "Not eating fruits and vegetables (< 2 pieces + < 300gram)",
            "Add+"]

#TODO: Connect to Database and add Edit functionality for user information
def profile_comp():
    return rx.flex(
            rx.avatar(src="/logo.jpg", fallback="NA", size="9"),
            rx.flex(
                rx.text("User Name", weight="bold", size="4"),
                rx.text("@username", color_scheme="gray"),
                rx.button(
                    "Edit Profile",
                    color_scheme="indigo",
                    variant="solid"
                ),
                direction="column",
                align="center",
                justify="center",
                padding_left='1rem'
            ),
            direction="row",
            spacing="1",
        )

def drainers_comp():
    return rx.grid(
        rx.foreach(
            ProfileState.drainers,
            lambda i: rx.card(i, height="5vh"),
        ),
        flow="row-dense",
        rows="10",
        spacing="4",
    )

def gainers_comp():
    return rx.grid(
        rx.foreach(
            ProfileState.gainers,
            lambda i: rx.card(i, height="5vh"),
        ),
        columns="3",
        spacing="4",
        width="100%"
    )

def goals_comp():
    return rx.text("Here goes goals")



"""The profile page."""

from ..templates import template
from ..components.profile_input import profile_input

# # Profile page, when not logged in
# @template(route="/login", title="Login")
# def login() -> rx.Component:
#     """The profile page to login.

#     Returns:
#         The UI for the login page.
#     """
#     return rx.vstack(
#         rx.flex(
#             rx.vstack(
#                 rx.hstack(
#                     rx.icon("square-user-round"),
#                     rx.heading("Login", size="5"),
#                     align="center",
#                 ),
#                 rx.text("User your email and password to login.", size="3"),
#                 width="100%",
#             ),
#             rx.form.root(
#                 rx.vstack(
#                     profile_input(
#                         label="User Email",
#                         name="email",
#                         placeholder="Email",
#                         type="text",
#                         icon="user",
#                         default_value="",
#                     ),
#                     profile_input(
#                         label="Password",
#                         name="password",
#                         placeholder="password",
#                         type="password",
#                         icon="mail",
#                         default_value="",
#                     ),
#                     rx.button("Login", type="submit", width="100%"),
#                     width="100%",
#                     spacing="5",
#                 ),
#                 on_submit=Authentication.handle_submit,
#                 # on_submit=lambda form_data: rx.window_alert(form_data.to_string()),
#                 reset_on_submit=True,
#                 width="100%",
#                 max_width="325px",
#             ),
#             rx.spacer(),
#             *[rx.spacer() for _ in range(2)],
#             rx.text(
#                 "Don't have an account? ",
#                 rx.link("Bet", href="/register"),"!"
#             ),
#             width="100%",
#             spacing="4",
#             flex_direction=["column", "column", "row"],
#         ),
#         rx.divider(),
#         spacing="6",
#         width="100%",
#         max_width="800px",
#     )


# Profile page, when logged in
@template(route="/profile", title="Profile")
def profile() -> rx.Component:
    """The profile page.

    Returns:
        The UI for the account page.
    """
    return rx.vstack(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon("square-user-round"),
                    rx.heading("Personal information", size="5"),
                    align="center",
                ),
                rx.text("Your personal information.", size="3"),
                width="100%",
            ),
            rx.flex(
                # TODO: Enable user profile picture upload
                rx.avatar(src="/logo.jpg", fallback="RU", size="9"),
                rx.text(Authentication.email, weight="bold", size="4"),
                rx.text(f"@{Authentication.username}", color_scheme="gray"),
                # TODO: Allow to update user information
                # rx.button(
                #     "Edit Profile",
                #     color_scheme="indigo",
                #     variant="solid",
                # ),
                rx.button("Logout",
                          on_click=Authentication.user_logout),
                direction="column",
                spacing="1",
            ),
            # rx.spacer(),
            # *[rx.spacer() for _ in range(2)],
            # rx.text(
            #     "Don't have an account? ",
            #     rx.link("Bet", href="/register"),"!"
            # ),
            width="100%",
            spacing="4",
            flex_direction=["column", "column", "row"],
        ),
        rx.divider(),
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon("bell"),
                    rx.heading("Notifications", size="5"),
                    align="center",
                ),
                rx.text("Manage your notification settings.", size="3"),
            ),
            rx.checkbox(
                "Receive product updates",
                size="3",
                # checked=ProfileState.profile.notifications,
                # on_change=ProfileState.toggle_notifications(),
            ),
            width="100%",
            spacing="4",
            justify="between",
            flex_direction=["column", "column", "row"],
        ),
        spacing="6",
        width="100%",
        max_width="800px",
    )
