import reflex as rx
from Journal.states import Authentication, State

def navbar():
    return rx.hstack(
        rx.button(
            rx.icon("undo-2"),
            size='1',
            on_click=rx.redirect("/notebook"),
        ),
        rx.hstack(
            rx.heading(
                "Evening Journal",
                font_size="2em",
                color="#184e47",
            ),
        ),
        rx.spacer(),
        # rx.button(rx.icon("sun-moon"), on_click=toggle_color_mode, variant="ghost", size="2"),
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    "Menu",
                    color="#eaf6f5",
                    background_color="#184e47",
                    # background_image="linear-gradient(#5fab7d, #a4daa6)",
                    # border="1px solid #eaf6f5",
                ),
            ),
            rx.menu.content(
                rx.menu.item(
                    "Logout",
                    on_click=Authentication.user_logout
                    ),
            ),
        ),
        position="fixed",
        top="0px",
        # background_color="#5fab7d",
        box_shadow= "0 4px 30px rgba(0, 0, 0, 0.1)",
        background_image="linear-gradient(0.25turn,#ffffff, #eaf6f5)",
        padding="1em",
        height="4em",
        width="100%",
        z_index="5",
    )

#TODO: Implement State for this
@rx.page('/profile/', on_load=State.void_event)
def profile_page():
    return rx.vstack(
        navbar(),
        rx.flex(
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
        ),
        rx.separator(size="3"),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Drainers & Gainers", value="tab1"),
                rx.tabs.trigger("Goals", value='tab2')
            ),
            rx.tabs.content(
                rx.text("Here goes Drainers and Gainers"),
                value="tab1"
            ),
            rx.tabs.content(
                rx.text("Here goes goals"),
                value="tab2"
            )
        ),
        padding_top="5rem",
        justify="center",
        align='center'
        # padding_left="1rem",
        # padding_right="1rem"
    )
