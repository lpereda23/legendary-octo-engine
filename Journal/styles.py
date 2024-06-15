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
    "width": ["100%", "100%", "70%", "50%", "35%"],
    "padding": ["1rem 1rem"],
    "transition": "all 550ms ease",
    "display": "flex",
    "justify_content": "center",
    "align-items": "center",
    "height": "45px",
}

auth_pages_stylesheet: dict = {
    "width": "100%",
    "height": "100vh",
    "display": "flex",
    "justify_content": "start",
    "align-items": "center",
}

post_card: dict = {
    "color":"ff0000",
    "background": 'rgba(255, 255, 255, 0.91)',
    "box-shadow": "0 4px 30px rgba(0, 0, 0, 0.1)",
    "backdrop-filter": "blur(17.2px)",
    "-webkit-backdrop-filter": "blur(17.2px)",
    "border-radius": "16px",
    "border": "1px solid rgba(255, 255, 255, 0.86)"
}
