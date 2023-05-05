from h2o_wave import main, app, Q, ui
from menus import SideMenu, SideMenuItem
from typing import List


side_menu_items = [
    SideMenuItem(
    group="1",
    name="home",
    label="Home",
    icon="Home",
    render=True,
    ),
    SideMenuItem(
    group="1",
    name="about",
    label="About",
    icon="cat",
    render=True,
    ),
    # SideMenuItem(
    # group="2",
    # name="help",
    # label="Help",
    # icon="Car",
    # render=True,
    # ),
]

def get_main_layout(q: Q):
    return ui.layout(
    breakpoint="",
    width=None,
    zones=[
        ui.zone("header"),
        ui.zone(
            name="main",
            direction=ui.ZoneDirection.ROW,
            zones=[
                        q.app.side_menu.layout,
                        ui.zone("main_body"),
                    ],
        ),
    ],
)

def app_layouts(template: ui.layout) -> List[ui.layout]:
    max_width = "1800px"
    configs = [("0px", "100%"), (max_width, max_width)]

    layouts: List[ui.layout] = []
    for b, w in configs:
        layout = template
        layout.breakpoint = b
        layout.width = w
        layouts.append(layout)
    return layouts

async def update_app_layout(q: Q):
    q.page["meta"] = ui.meta_card(
    box="",
    title="Side-menu Tutorial",
    layouts=app_layouts(get_main_layout(q)),
)

async def init_app(q: Q):
    if q.app.initialised:
        return
    q.app.side_menu = SideMenu(items=side_menu_items, collapsable=True)
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
        q.page['example'] = ui.form_card(box='main_body',
                                    items=[
                                        ui.text("Home"),
                                    ])
    elif q.app.active_page == "about":
        q.page['example'] = ui.form_card(box='main_body',
                                    items=[
                                        ui.text("About")
                                    ])
@app('/demo')
async def serve(q: Q): 
    print(f"q.args: {q.args}")  # Logging
    await init_app(q)
    await handle_args(q)
    await update_app_layout(q)
    await render_sidemenu(q)
    await render_cards(q)
    await q.page.save()