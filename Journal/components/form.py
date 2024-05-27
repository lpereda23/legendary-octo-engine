import reflex as rx
from Journal.states import Post


def render_post_form():
    return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Submit New Journal Entry"),
                rx.spacer(),
                rx.input(
                        placeholder="Intention(s):",
                        margin="0.5rem 0rem",
                        value=Post.post_intention,
                        on_change=Post.update_post_intention
                ),
                rx.spacer(),
                rx.input(
                        placeholder="Success(es):",
                        margin="0.5rem 0rem",
                        value=Post.post_success,
                        on_change=Post.update_post_success
                ),
                rx.spacer(),
                rx.input(
                        placeholder="Lesson(s):",
                        margin="0.5rem 0rem",
                        value=Post.post_lesson,
                        on_change=Post.update_post_lesson
                ),
                rx.spacer(),
                rx.input(
                        placeholder="Grateful for:",
                        margin="0.5rem 0rem",
                        value=Post.post_grateful,
                        on_change=Post.update_post_grateful
                ),
                rx.spacer(),
                # padding="0.25rem 1rem"

                rx.vstack(
                        rx.heading(
                            f"Lessons Score: {Post.post_lesson_score}",
                            size="4"
                        ),
                        rx.slider(
                            default_value=0,
                            value=[Post.post_lesson_score],
                            on_change=Post.update_post_lesson_score,
                        ),
                        rx.spacer(),
                        rx.heading(
                            f"Successes Score: {Post.post_success_score}",
                            size="4"
                        ),
                        rx.slider(
                            default_value=0,
                            value=[Post.post_success_score],
                            on_change=Post.update_post_success_score,
                        ),
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            on_click=Post.toggle_post_form
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Submit",
                            on_click=Post.submit_post_for_validation
                        ),
                    ),
                    spacing='3',
                    margin_top="16px",
                    justify="end"

                )
            ),
            open=Post.is_open
        )
