"""Styles for the app."""

general_stylesheet: dict = {
    "width": ["100%", "100%", "70%", "50%", "35%"],
    "padding": ["0rem 2rem"],
    "transition": "all 550ms ease",
    "display": "flex",
    "justify_content": "start",
    "align-items": "center",
}

input_stylesheet: dict = {
    **general_stylesheet

}

button_stylesheet: dict = {
    **general_stylesheet,
    "height": "45px",
}

auth_pages_stylesheet: dict = {
    "width": "100%",
    "height": "100vh",
    "display": "flex",
    "justify_content": "start",
    "align-items": "center",
}
