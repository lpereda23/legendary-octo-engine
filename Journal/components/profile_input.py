import reflex as rx


def profile_input(
    label: str,
    name: str,
    placeholder: str,
    type: str,
    icon: str,
    default_value="",
    # value = rx.Var,
    # update = rx.State
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=16, stroke_width=1.5),
            rx.text(label),
            width="100%",
            align="center",
            spacing="2",
        ),
        rx.input(
            placeholder=placeholder,
            # value=value,
            default_value="",
            # update=update,
            type=type,
            width="100%",
            name=name,
        ),
        direction="column",
        spacing="1",
        width="100%",
    )
