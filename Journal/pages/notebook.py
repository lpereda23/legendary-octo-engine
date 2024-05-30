# main notebook page...

import reflex as rx
from reflex.style import toggle_color_mode
from Journal.components.form import render_post_form
from Journal.states import Authentication, JournalData, Comments, Post
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
            rx.heading("Evening Journal", font_size="2em"),
        ),
        rx.spacer(),
        rx.button(rx.icon("sun-moon"), on_click=toggle_color_mode, variant="ghost", size="2"),
        rx.menu.root(
            rx.menu.trigger(
                rx.button("Menu"),
            ),
            rx.menu.content(
                rx.menu.item(
                    "New Journal Entry",
                    on_click=Post.toggle_post_form),
                rx.menu.separator(),
                rx.menu.item(
                    "Logout",
                    on_click=Authentication.user_logout
                    ),
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
        reusable_meta_data_component(
            _tag="at_sign", _label="Username", _name=username,
            fn=Comments.void_event
        ),
        reusable_meta_data_component(
            _tag="clock", _label="Created On", _name=time,
            fn=Comments.void_event
        ),
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
        spacing="2",
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
            justify_content="start",
            align_items="center",
            spacing="2"
        ),
        width="100%",
        display="flex",
        padding_left="0.75rem",
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
            ),
            spacing='3'
        ),
        border_radius="15px",
        background_color="#f2f2f2",
        # box_shadow="0px 0px 3px 2px #132a3e",
        justify="start",
        align="center",
        width="100%"
    )

@rx.page("/notebook", on_load=JournalData.on_notebook_landing_event)
def notebook():
    return rx.vstack(
        #post form goes here
        render_post_form(),
        navbar(),
        rx.vstack(
            rx.foreach(
                    JournalData.posts,
                    render_fn=render_item
            ),

            width="100%",
            align="center",
            padding_top="5rem",
            padding_left="1rem",
            padding_right="1rem",
            # padding="5rem 2rem",
            overflow="auto",
            transition="all 550ms ease",
        ),
        rx.spacer(),
        align="center",
        width="100%",
    )
