from pathlib import Path
from typing import List

from h2o_wave import Q, app, main, ui  # noqa F401

from menus import SideMenu, SideMenuItem

app_layoutsize: str = "1000px"  # Change this to change the size of the layout
stylesheet = ui.InlineStylesheet(
    Path("common.css").read_text()
)  # CSS file for styling. Spefically for spacing between different nav_groups without group names


side_menu_items: List[SideMenuItem] = [
    SideMenuItem(
        name="home",
        label="Home",
        group="Group 1",
        icon="Home",
        render=True,
        sub_items=[
            SideMenuItem(
                name="subpage",
                label="Subpage",
                icon="model",
                render=False,
            ),
            SideMenuItem(
                name="subpage2",
                label="Subpage 2",
                icon="model",
                render=False,
            ),
        ],
    ),
    SideMenuItem(
        name="about",
        label="About",
        group="Group 1",
        icon="cat",
        render=True,
    ),
]


async def update_app_layout(q: Q):
    """Update the app layout based on the state of the side menu"""
    app_layout = ui.layout(
        breakpoint=app_layoutsize,
        width=app_layoutsize,
        zones=[
            ui.zone("header"),
            ui.zone(
                name="main",
                direction=ui.ZoneDirection.ROW,
                zones=[
                    q.app.side_menu.layout,  # Sidemenu layout info changes based on the state of collapsed or not
                    ui.zone("main_body"),
                ],
            ),
        ],
    )

    q.page["meta"] = ui.meta_card(
        box="",
        title="Side-menu Tutorial",
        layouts=[app_layout],
        stylesheet=stylesheet,
    )


async def init_app(q: Q):
    """Initialise the app"""
    if q.app.initialised:
        return
    q.app.side_menu = SideMenu(items=side_menu_items, collapsable=True, disable_group_names=True)
    q.app.active_page = "home"
    q.app.initialised = True


async def handle_args(q: Q):
    """Handle the arguments passed to the app"""
    if q.args["side_menu_toggle_collapse"]:
        q.app.side_menu.toggle_state()
    elif q.args["subpage"]:
        q.app.side_menu.disable_subitems()
        root_item = q.app.side_menu.get_root_item("subpage")
        q.app.side_menu.enable_subitems(root_item.name)
        q.app.side_menu.active_root_item = root_item
        q.app.side_menu.expand_root_item = True
        q.app.active_page = "subpage"
    elif q.args["subpage2"]:
        q.app.side_menu.disable_subitems()
        root_item = q.app.side_menu.get_root_item("subpage2")
        q.app.side_menu.enable_subitems(root_item.name)
        q.app.side_menu.active_root_item = root_item
        q.app.side_menu.expand_root_item = True
        q.app.active_page = "subpage2"
    elif q.args["home"]:
        q.app.side_menu.expand_root_item = False
        q.app.side_menu.active_root_item = q.app.side_menu.get_item("home")
        q.app.side_menu.disable_subitems()
        q.app.active_page = "home"
    elif q.args["about"]:
        q.app.side_menu.expand_root_item = False
        q.app.side_menu.active_root_item = q.app.side_menu.get_item("about")
        q.app.side_menu.disable_subitems()
        q.app.active_page = "about"


async def render_sidemenu(q: Q):
    """Render the side menu"""
    q.page["sidemenu"] = ui.nav_card(
        box=ui.box(zone="sidebar", width=q.app.side_menu.width, height=q.app.side_menu.height),
        items=q.app.side_menu.get_nav_content(q=q),
        value=q.app.active_page,
    )


async def render_cards(q: Q):
    """Render the cards based on the active page"""
    if q.app.active_page == "home":
        q.page["example"] = ui.form_card(
            box=ui.box(zone="main_body", height="500px"),
            items=[
                ui.text(
                    "<h3 style='font-size:1.5vw'>Welcome to Collapsable SideMenu tutorial!</h3>"
                ),
                ui.buttons(
                    items=[
                        ui.button(name="subpage", label="Open Subpage", primary=True),
                        ui.button(name="subpage2", label="Open Subpage 2", primary=True),
                    ]
                ),
            ],
        )
    elif q.app.active_page == "about":
        q.page["example"] = ui.form_card(
            box=ui.box(zone="main_body", height="500px"),
            items=[ui.text("SideMenu object can be used only in H2O Wave projects")],
        )
    elif q.app.active_page == "subpage":
        q.page["example"] = ui.form_card(
            box=ui.box(zone="main_body", height="500px"), items=[ui.text("Subpage")]
        )
    elif q.app.active_page == "subpage2":
        q.page["example"] = ui.form_card(
            box=ui.box(zone="main_body", height="500px"), items=[ui.text("Subpage 2")]
        )


@app("/demo")
async def serve(q: Q):
    """Main app function"""
    print(f"q.args: {q.args}")  # Logging
    await init_app(q)
    await handle_args(q)
    await update_app_layout(q)
    await render_sidemenu(q)
    await render_cards(q)
    await q.page.save()
