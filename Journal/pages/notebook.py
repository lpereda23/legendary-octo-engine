# main notebook page...

import reflex as rx
from reflex.style import toggle_color_mode
from Journal.states import JournalData
from Journal.models import CustomPost

def switch_theme_color():
    return {
        "_dark": {"color":"white"},
        "_light": {"color": "white"}
    }

def navbar():
    return rx.hstack(
        rx.hstack(
            # rx.image(src="/favicon.ico", width="2em"),
            rx.heading("Journal App", font_size="2em"),
        ),
        rx.spacer(),
        rx.button(rx.icon("sun-moon"), on_click=toggle_color_mode, variant="ghost", size="2"),
        rx.menu.root(
            rx.menu.trigger(
                rx.button("Menu"),
            ),
            rx.menu.content(
                rx.menu.item("New Journal Entry"),
                rx.menu.separator(),
                rx.menu.item("Logout"),
            ),
        ),
        position="fixed",
        top="0px",
        background_color="lightgray",
        padding="1em",
        height="4em",
        width="100%",
        z_index="5",
    )

def render_post_header(item: str):
    return rx.accordion.root(
        rx.accordion.item(
            header=item.title,
            content=item.content
            )
        )

def render_item(item: CustomPost):
    print(item)
    return rx.text(item.title)

@rx.page("/notebook", on_load=JournalData.on_notebook_landing_event)
def notebook():
    return rx.fragment(
        navbar(),
        rx.vstack(
            rx.foreach(
                    JournalData.posts,
                    render_fn=render_item
            ),

            width="100%",
            padding="5rem 1rem",
            overflow="auto",
            transition="all 550ms ease"
        ),
        rx.spacer(),
        width="100%",
    )
