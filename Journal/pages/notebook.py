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
            rx.heading("Journal App", font_size="2em"),
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

def render_post_header(item: str):
    return rx.chakra.accordion_button(
        rx.heading(item, size="2", text_align="start"),
        rx.spacer(),
        rx.chakra.accordion_icon()
    )

def render_post_content(data: str):
    """
        Render content of the post
    """
    return [
        rx.text(
            data,
            text_align="start",
            font_size={"13px","13px","14px","15px","15px",},
            transition="all 550ms ease",
        ),
        rx.box(rx.divider(opacity="0"), padding="1em 0em")
    ]

def render_item(item: CustomPost):
    return rx.chakra.accordion(
        rx.chakra.accordion_item(
            render_post_header(item.title),
            rx.chakra.accordion_panel(
                # * unpacks list of components
                *render_post_content(item.content),
                *render_post_comment_form(item),
                rx.hstack(
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
                rx.divider(height="2", opacity="0"),
                rx.vstack(
                    # This iterator renders the comments
                    rx.foreach(
                        # NOTE: item.comments is a list[dict]
                        iterable=item.comments,
                        render_fn=render_comments
                    ),
                    width="100%",
                    display="flex",
                    justify="center",
                    align="center",
                    spacing="1"
                ),
            ),
            padding="0.25em 0em",
            margin="0",
            overflow="hidden",
            border="1px 0px 1px 0px solid gray"
        ),
        width=["100%", "100%", "80%", "65%", "60%"],
        allow_multiple=True,
        padding="0.65rem 0rem",
        overflow="hidden",
        reduce_motion=True,
        transition="all 550ms ease"
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
            padding="5rem 1rem",
            overflow="auto",
            transition="all 550ms ease"
        ),
        rx.spacer(),
        width="100%",
    )
