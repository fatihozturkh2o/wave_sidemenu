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
    ]
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

async def update_app_layout(q: Q):
    app_layout = ui.layout(
    breakpoint="1800px",
    width="1800px",
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

    q.page["meta"] = ui.meta_card(
    box="",
    title="Side-menu Tutorial",
    layouts=[app_layout],
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
                                        ui.button(name="subpage", label="Subpage", primary=True),
                                        ui.button(name="subpage2", label="Subpage 2", primary=True)

                                    ])
    elif q.app.active_page == "about":
        q.page['example'] = ui.form_card(box='main_body',
                                    items=[
                                        ui.text("About")
                                    ])
    elif q.app.active_page == "subpage":
        q.page['example'] = ui.form_card(box='main_body',
                                    items=[
                                        ui.text("Subpage")
                                    ])
    elif q.app.active_page == "subpage2":
        q.page['example'] = ui.form_card(box='main_body',
                                    items=[
                                        ui.text("Subpage 2")
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