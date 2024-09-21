# main notebook page...

import reflex as rx
from reflex.style import toggle_color_mode
from Journal.components.speed_dial import render_reveal
from Journal.styles import post_card
from Journal.components.form import render_post_form
from Journal.states import Authentication, JournalData, Comments, Post
from Journal.models import CustomPost
from datetime import datetime

def switch_theme_color():
    return {
        "_dark": {"color":"white"},
        "_light": {"color": "white"}
    }

def navbar():
    return rx.hstack(
        rx.hstack(
            # rx.image(src="/favicon.ico", width="2em"),
            rx.heading(
                "Evening Journal",
                font_size="2em",
                color="#374B43",
                # box_shadow= "0 4px 30px rgba(0, 0, 0, 0.1)",
            ),
        ),
        rx.spacer(),
        # rx.button(rx.icon("sun-moon"), on_click=toggle_color_mode, variant="ghost", size="2"),
        rx.menu.root(
            rx.menu.trigger(
                rx.icon_button(
                    rx.icon("user"),
                    size="2",
                    radius="full",
                    color="#eaf6f5",
                    background_color="#374B43",
                ),
            ),
            rx.menu.content(
                rx.menu.item(
                    "New Journal Entry",
                    on_click=Post.toggle_post_form),
                rx.menu.item(
                    "Stats",
                    on_click=rx.redirect(
                        "/stats"
                    ),
                ),
                rx.menu.item(
                    "Account",
                    on_click=rx.redirect(
                        "/profile"
                    )
                ),
                rx.menu.separator(),
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

def render_post_comment_form(item: CustomPost) -> list:
    """ Renders the comment section of a post
        With the option to comment on post and update on db
    """
    return [
        rx.text(
            "Comments",
            font_size = "12px",
            opacity="0.01",
            display=item.is_comment_visible,
        ),
        rx.box(
            rx.divider(opacity="0"),
            padding="0.25em 10em",
            display=item.is_comment_visible
        ),
        rx.text_area(
            value=Comments.post_comment,
            placeholder="Enter your comment here ...",
            display=item.is_comment_visible,
            on_change=Comments.update_post_comment,
        ),
        rx.box(
            rx.divider(opacity="0"),
            padding="0.25em 10em",
            display=item.is_comment_visible
        ),
        rx.box(
            rx.button(
                "Comment",
                display=item.is_comment_visible,
                on_click=Comments.commit_comment_to_post(item),
            ),
            display='flex',
            justify_content="end",
            width="100%",
        ),
        rx.box(
            rx.divider(opacity="0"),
            padding="1em 10em",
            display=item.is_comment_visible
        ),
    ]

# The following renders the META DATA for each post -> timestamp, userName and toggle_comment
def reusable_meta_data_component(_tag: str, _label: str, _name : str, fn: callable):
    return rx.hstack(
        rx.tooltip(
            rx.icon(
                tag=_tag,
                transform="Scale(0.7)",
                opacity="0.8",
                cursor="pointer",
                on_click=fn
            ),
            content=_label,
            _dark={"bg":"#1b1b1b", "color":"white"},
            _light={"bg":"#ffffff", "color":"black"},
        ),
        rx.text(
            _name,
            opacity="0.8",
            font_size="10px"
        ),
        spacing="0",
        display="flex",
        align="center",
        justify="start",
    )

# Next is to render the POST METADATA, similar to the method above
def render_post_metadata(time: str, username: str, item: CustomPost):
    return rx.hstack(
        # reusable_meta_data_component(
        #     _tag="at_sign", _label="Username", _name=username,
        #     fn=Comments.void_event
        # ),
        # reusable_meta_data_component(
        #     _tag="clock", _label="Created On", _name=time,
        #     fn=Comments.void_event
        # ),
        rx.cond(
            condition=item.is_comment_visible == "none",
            c1=reusable_meta_data_component(
                _tag="pencil",
                _label="Comment",
                _name="Leave a comment",
                fn=Comments.toggle_comment(item)
            ),
            c2=reusable_meta_data_component(
                _tag="circle-x",
                _label="Comment",
                _name="Close comment",
                fn=Comments.toggle_comment(item),
            ),
        ),
        padding=".25rem",
        spacing="2",
        justify_content="space_between"
    )

# Finally have the component that renders the comments by other users
def render_comments(item):
    return rx.vstack(
        rx.hstack(
            rx.text(item.content),
            width="100%",
            display="flex",
            justify_content="start",
            align_items="center",
        ),
        rx.hstack(
            reusable_meta_data_component(
                _tag="at_sign", _label="Username", _name=item.username,
                fn=Comments.void_event
            ),
            reusable_meta_data_component(
                _tag="clock", _label="Created On", _name=item.created_at,
                fn=Comments.void_event
            ),
            width="100%",
            display="flex",
            justify_content="end",
            align_items="end",
            padding=".25rem",
            spacing="2"
        ),
        rx.divider(size="3"),
        spacing="1",
        width="100%",
        display="flex",
        padding_left="1rem",
        _dark={"border_left":"1px solid gray"},
        _light={"border_left":"1px solid black"}
    )

def render_post_header(time: str, username: str):
    return rx.hstack(
        reusable_meta_data_component(
            _tag="at_sign", _label="Username", _name=username,
            fn=Comments.void_event
        ),
        reusable_meta_data_component(
            _tag="clock", _label="Created On", _name=time,
            fn=Comments.void_event
        ),
        spacing="4",
        padding="4px",
        justify="between"
    )

def render_post_content(intention: str,
                        success: str,
                        lesson: str, grateful: str):
    """
        Render content of the post
    """
    return [
            rx.vstack(
                rx.box(
                    rx.heading("Intention(s):", size="2", weight="light"),
                    rx.text(intention),
                    width="100%",
                    padding="7px"
                ),
                rx.box(
                    rx.heading("Success(es):", size="2", weight="light"),
                    rx.text(success),
                    width="100%",
                    padding="7px"
                ),
                rx.box(
                    rx.heading("Lesson(s):", size="2", weight="light"),
                    rx.text(lesson),
                    width="100%",
                    padding="7px"
                ),
                rx.box(
                    rx.heading("Grateful:", size="2", weight="light"),
                    rx.text(grateful),
                    width="100%",
                    padding="7px"
                ),
        )
    ]

def filter_render_item(item: CustomPost):
    if (datetime.fromtimestamp(item.created_at) >=
        datetime.fromtimestamp(JournalData.start_date)) and (datetime.fromtimestamp(item.created_at) <=
        datetime.fromtimestamp(JournalData.end_date)):
            render_item(item)

def render_item(item: CustomPost):
    return rx.flex(
        rx.vstack(
            rx.box(
                render_post_header(
                    item.created_at,
                    item.username
                ),
                *render_post_content(
                    item.intention, item.success,
                    item.lesson, item.grateful
                ),
                *render_post_comment_form(item),
                rx.flex(
                    render_post_metadata(
                        item.created_at,
                        item.username,
                        item
                    ),
                    width="100%",
                    display="flex",
                    justify="end",
                    align="center"
                ),
                rx.divider(size="4"),
                rx.vstack(
                    rx.foreach(
                        iterable=item.comments,
                        render_fn=render_comments
                    ),
                    width="100%",
                    display="flex",
                    justify="center",
                    align="center",
                    spacing="1"
                ),
                width="100%"

            ),
            width="100%",
            spacing='3',
        ),
        spacing="4",

        style=post_card,
        justify="center",
        align="center",
        width="100%"
    )


def form_field(
    label: str, placeholder: str, type: str, name: str
    ) -> rx.Component:
    return rx.form.field(
        rx.flex(
            # rx.form.label(label),
            rx.form.control(
                rx.input(
                    placeholder=placeholder, type=type
                ),
                as_child=True
            ),
            direction="column",
            spacing='1',
        ),
        name=name,
        width="100%"
    )

def event_form() -> rx.Component:
    return rx.card(
        rx.flex(
            # rx.hstack(
            #     rx.badge(
            #         rx.icon(tag="calendar-plus", size=32),
            #         color_scheme="mint",
            #         radius="full",
            #         padding="0.65rem",
            #     ),
            #     height="100%",
            #     spacing="4",
            #     align_items="center",
            #     width="100%",
            # ),
            rx.form.root(
                rx.flex(
                    rx.flex(
                        form_field(
                            "Date", "", "date", "event_start"
                        ),
                        form_field(
                            "Date", "", "date", "event_end"
                        ),
                        spacing="5",
                        flex_direction="row",
                        justify='between',
                        width="100%"
                    ),
                    direction="column",
                    spacing="2",
                ),
                rx.form.submit(
                    rx.button("Set Date Range"),
                    as_child=True,
                    width="100%",
                ),
                on_submit=lambda form_data: JournalData.set_date_filter(form_data
                ),
                reset_on_submit=False,
            ),
            width="100%",
            direction="column",
            spacing="4",
        ),
        size="3",
    )

def filter_dialog() -> rx.Component:
    """
    Dialog to select filters for Journal entries, on notebook
    """
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Filter", variant="soft")),
        rx.dialog.content(
            rx.dialog.title("Select Date Range"),
            rx.dialog.description("Display journal entries between selected dates"),
            event_form(),
            rx.flex(
                rx.dialog.close(
                rx.button("Close", size="3", variant="soft"),
                ),
                justify="end",
                margin_top="1em"
            )

        ),
    )

"""--------------------new ui------------------------------------------------------------------------------"""
from ..templates import template

@template(route="/notebook", title="Notebook", on_load=JournalData.on_notebook_landing_event)
def notebook() -> rx.Component:
    """
    The page for all Journal Entries
    Returns: The UI for the notebook page.
    """
    return rx.vstack(
        rx.hstack(
            rx.heading("All your Entries", size="4"),
            filter_dialog(),
            direction="row",
            justify="between",
            spacing="3",
            width="100%",
        ),
        render_post_form(),
        render_reveal(),

        rx.stack(
            rx.foreach(
                JournalData.posts,
                render_fn=render_item
            ),
            width="100%",
            align="center",
            direction="column-reverse",

        ),

        width="100%"

    )
