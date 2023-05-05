from pathlib import Path

from h2o_wave import Q, app, main, ui  # noqa F401

from menus import SideMenu, SideMenuItem

app_layoutsize: str = "1000px"
stylesheet = ui.InlineStylesheet(Path("common.css").read_text())

side_menu_items = [
    SideMenuItem(
        name="home",
        label="Home",
        group="Group 1",
        icon="Home",
        render=True,
    ),
    SideMenuItem(
        name="about",
        label="About",
        group="Group 1",
        icon="cat",
        render=True,
    ),
    SideMenuItem(
        name="new_group_item_1",
        label="New Group Item 1",
        group="Group 2",
        icon="CoffeeScript",
        render=True,
    ),
    SideMenuItem(
        name="new_group_item_2",
        label="New Group Item 2",
        group="Group 2",
        icon="CoffeeScript",
        render=True,
    ),
]


async def update_app_layout(q: Q):
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
    if q.app.initialised:
        return
    q.app.side_menu = SideMenu(items=side_menu_items, collapsable=True, disable_group_names=True)
    q.app.active_page = "home"
    q.app.initialised = True


async def handle_args(q: Q):
    if q.args["side_menu_toggle_collapse"]:
        q.app.side_menu.toggle_state()
    elif q.args["home"]:
        q.app.active_page = "home"
    elif q.args["about"]:
        q.app.active_page = "about"


async def render_sidemenu(q: Q):
    q.page["sidemenu"] = ui.nav_card(
        box=ui.box(zone="sidebar", width=q.app.side_menu.width, height=q.app.side_menu.height),
        items=q.app.side_menu.get_nav_content(q=q),
        value=q.app.active_page,
    )


async def render_cards(q: Q):

    if q.app.active_page == "home":
        q.page["example"] = ui.form_card(
            box=ui.box(zone="main_body", height="500px"),
            items=[
                ui.text(
                    "<h3 style='font-size:1.5vw'>Welcome to Collapsable SideMenu tutorial!</h3>"
                ),
            ],
        )
    elif q.app.active_page == "about":
        q.page["example"] = ui.form_card(
            box=ui.box(zone="main_body", height="500px"),
            items=[ui.text("SideMenu object can be used only in H2O Wave projects")],
        )


@app("/demo")
async def serve(q: Q):
    print(f"q.args: {q.args}")  # Logging
    await init_app(q)
    await handle_args(q)
    await update_app_layout(q)
    await render_sidemenu(q)
    await render_cards(q)
    await q.page.save()
