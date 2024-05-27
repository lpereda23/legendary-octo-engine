import reflex as rx
from Journal.states import Post

def render_post_form():
    return rx.chakra.modal(
        rx.chakra.modal_overlay(
            rx.chakra.modal_content(
                rx.chakra.modal_header("Submit Post"),
                rx.chakra.modal_body(
                    rx.input(
                        placeholder="Post Title",
                        margin="0.5rem 0rem",
                        value=Post.post_title,
                        on_change=Post.update_post_title
                    ),
                    rx.spacer(),
                    rx.input(
                        placeholder="Post Body",
                        margin="0.5rem 0rem",
                        value=Post.post_body,
                        on_change=Post.update_post_body
                    ),
                    padding="0.25rem 1rem"
                ),
                rx.chakra.modal_footer(
                    rx.hstack(
                        rx.chakra.button(
                            "Close",
                            on_click=Post.toggle_post_form
                        ),
                        rx.chakra.button(
                            "Submit",
                            on_click=Post.submit_post_for_validation
                        )
                    )
                )
            )
        ),
        is_open=Post.is_open
    )
