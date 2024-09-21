import reflex as rx
from Journal.states import Authentication, State


class ProfileState(rx.State):
    gainers = ["Music", "Nature", "Cuddling a/your pet", "Grounding(bare feet walk)", "Eating clean healthy nutrition",
                "Good night sleep", "Offline time", "Quality time with a (positive) good friend", "Meditate",
                "Breathwork", "Just sit still (and stare at nature/the clouds/the grass)", "Breathwork",
                "Workout", "Stretch", "Go to Spa", "Go on a week(end) trip", "Journal your thoughts",
                "Write down your dreams and visualize them", "Read", "Learn something new (a course / seminar / youtube)",
                "Dance (like no one's watching)", "Have sex", "Take a nap",
                "Saying no (so you say even more YESSS to what is really important to you)",
                "Add+"]
    drainers = ["Being around synic / negative / complaining / harsh / dominating people",
               "Saying yes to everything and everyone", "No time management", "Reactive behavior",
               "Not being reliable to your own word with respect to others BUT EVEN MORE TOWARDS YOUR OWN WORD",
                "Going to bed too late", "Sleeping inconsistent", "Not having enough hours of sleep (i.e. < 7,5 hours)",
                "Eating processed foods // rich of sugar // rich of saturated fats", "Sitting still whole day",
                "Being inside the whole day",
                "Doom scrolling and other dopamine kick habits (and out of a sudden don't have enough time to work on your goals anymore...)",
                "Procrastination of important tasks", "Snoozing", "Warm long morning showers during working days",
                "Having calories within 2 hours before sleep", "Not having a morning AND evening routine",
                " Dehydration (< 2L of water)", "Drinking > 4 cups of coffee",
                "Drinking alcohol (Short run: affects your sleep quality, sharpness, energy, mood; Long run affects your quality of life, health and perception of your mood",
                "Not eating fruits and vegetables (< 2 pieces + < 300gram)",
                "Add+"]

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

#TODO: Connect to Database and add Edit functionality for user information
def profile_comp():
    return rx.flex(
            rx.avatar(src="/logo.jpg", fallback="NA", size="9"),
            rx.flex(
                rx.text("User Name", weight="bold", size="4"),
                rx.text("@username", color_scheme="gray"),
                rx.button(
                    "Edit Profile",
                    color_scheme="indigo",
                    variant="solid"
                ),
                direction="column",
                align="center",
                justify="center",
                padding_left='1rem'
            ),
            direction="row",
            spacing="1",
        )

def drainers_comp():
    return rx.grid(
        rx.foreach(
            ProfileState.drainers,
            lambda i: rx.card(i, height="5vh"),
        ),
        flow="row-dense",
        rows="10",
        spacing="4",
    )

def gainers_comp():
    return rx.grid(
        rx.foreach(
            ProfileState.gainers,
            lambda i: rx.card(i, height="5vh"),
        ),
        columns="3",
        spacing="4",
        width="100%"
    )

def goals_comp():
    return rx.text("Here goes goals")


#TODO: Implement State for this
@rx.page('/profile/', on_load=State.void_event)
def profile_page():
    return rx.vstack(
        navbar(),
        profile_comp(),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Drainers", value="tab1"),
                rx.tabs.trigger("Gainers", value="tab2"),
                rx.tabs.trigger("Goals", value='tab3')
            ),
            rx.tabs.content(
                drainers_comp(),
                padding_top="1rem",
                value="tab1"
            ),
            rx.tabs.content(
                gainers_comp(),
                padding_top="1rem",
                value="tab2"
            ),
            rx.tabs.content(
                goals_comp(),
                padding_top="1rem",
                value="tab3"
            ),
            width="100%",
            padding_top="1rem",
            padding="1rem"
        ),
        padding_top="5rem",
        justify="center",
        align='center'
    )
