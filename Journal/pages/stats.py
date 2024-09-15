# Page to review stats for journaling
import reflex as rx
from Journal.states import Authentication, Post, StatsState

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
                    "New Journal Entry",
                    on_click=Post.toggle_post_form),
                rx.menu.item(
                    "Stats",
                    on_click=Post.toggle_post_form
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

@rx.page('/stats', on_load=Stats.on_stats_landing_event)
def stats_page():
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.text("Lesson and Success Scores"),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    data_key="lesson_score",
                    stroke="#8884d8", fill="#8884d8",
                    label=True
                ),
                rx.recharts.bar(
                    data_key="success_score",
                    stroke="#82ca9d", fill="#82ca9d",
                    label=True
                ),
                rx.recharts.x_axis(data_key="created_at"),
                rx.recharts.y_axis(),
                rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                rx.recharts.graphing_tooltip(),
                rx.recharts.legend(),
                data=Stats.posts,
                height=300,
            ),
            pading_top="1rem",
            pading_left="1rem",
            padding_right="1rem",
            align="center",
            width="100%"

        ),
        padding_top="10rem",
        # padding_left="1rem",
        # padding_right="1rem"
    )
