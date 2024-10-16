import reflex as rx
from Journal.styles import button_stylesheet

def render_submit_button(name: str, event: rx.State) -> None:
    return rx.hstack(
        rx.button(
            rx.text(name),
            on_click=event,
            width="80%",
            background_color="#374B43",
        ),
        style=button_stylesheet,
        # padding="0.05 rem 0rem"
    )
