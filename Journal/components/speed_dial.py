import reflex as rx

from Journal import styles
from Journal.states import Post

class SpeedDialReveal(rx.ComponentState):
    is_open: bool = False

    def toggle(self, value: bool):
        self.is_open = value

    @classmethod
    def get_component(cls, **props):
        def menu_item(icon: str, text: str) -> rx.Component:
            return rx.tooltip(
                rx.icon_button(
                    rx.icon(icon, padding="2px"),
                    on_click=Post.toggle_post_form,
                    variant="soft",
                    color_scheme="gray",
                    size="3",
                    cursor="pointer",
                    radius="full",
                    style={
                        "animation": rx.cond(
                            cls.is_open,
                            "reveal 0.3s ease both",
                            "none",
                        ),
                        "@keyframes reveal": {
                            "0%": {
                                "opacity": "0",
                                "transform": "scale(0)",
                            },
                            "100%": {
                                "opacity": "1",
                                "transform": "scale(1)",
                            },
                        },
                    },
                ),
                side="left",
                content=text,
            )

        def menu() -> rx.Component:
            return rx.vstack(
                menu_item("copy", "Journal"),
                # menu_item("download", "Download"),
                # menu_item("share-2", "Share"),
                position="absolute",
                bottom="100%",
                spacing="2",
                padding_bottom="10px",
                left="0",
                direction="column-reverse",
                align_items="center",
            )

        return rx.box(
            rx.box(
                rx.icon_button(
                    rx.icon(
                        "plus",
                        style={
                            "transform": rx.cond(
                                cls.is_open,
                                "rotate(45deg)",
                                "rotate(0)",
                            ),
                            "transition": "transform 150ms cubic-bezier(0.4, 0, 0.2, 1)",
                        },
                        class_name="dial",
                    ),
                    variant="solid",
                    color=styles.accent_color,
                    size="3",
                    cursor="pointer",
                    radius="full",
                    position="relative",
                ),
                rx.cond(
                    cls.is_open,
                    menu(),
                ),
                position="relative",
            ),
            on_mouse_enter=cls.toggle(True),
            on_mouse_leave=cls.toggle(False),
            on_click=cls.toggle(~cls.is_open),
            style={"bottom": "15px", "right": "15px"},
            position="absolute",
            z_index="50",
            **props,
        )


speed_dial_reveal = SpeedDialReveal.create


def render_reveal():
    return rx.box(
        speed_dial_reveal(),
        # height="250px",
        position="fixed",
        width="100%",
        bottom="2em",
        right="2em",
        padding_bottom="15px",
        z_index="100"
    )
