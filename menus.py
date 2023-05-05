from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

import numpy as np
from h2o_wave import Q, ui
from h2o_wave.types import Zone


@dataclass
class SideMenuItem:
    group: Optional[str] = None  # wave attribute, display items based on their groups
    name: Optional[str] = None  # wave attribute, name for handling click operations
    label: Optional[str] = None  # wave attribute, label to display
    icon: Optional[str] = "ChevronRightMed"  # wave attribute, icon to display
    expanded_icon: Optional[str] = "ChevronDownMed"  # expanded icon to display
    disabled: Optional[bool] = False  # wave attribute
    expand_always: Optional[bool] = False  # always expand and render sub items
    render: Optional[bool] = False  # render item
    sub_items: Optional[List] = field(default_factory=list)  # assign sub items


class SideMenu:
    def __init__(
        self,
        items: Optional[List[SideMenuItem]] = None,
        collapsed: bool = False,
        collapsable: bool = True,
        auto_width: bool = True,
        documentation: bool = False,
    ):
        self.collapsed = collapsed
        self.collapsable = collapsable
        self.documentation = documentation
        self.items = items or []
        self.active_root_item: Optional[SideMenu] = None
        self.expand_root_item: bool = False
        self._documentation_icon: str = "Documentation"
        self._documentation_label: str = "Documentation"
        self._auto_width: bool = auto_width
        self._min_width: int = 200
        self._max_width: int = 300
        self._width: List[str] = ["210px", "48px"]
        self._height: str = "100%"
        self._collapse_button_icon: List[str] = ["DoubleChevronLeft8", "DoubleChevronRight8"]
        self._collapsed_item_label: str = ""
        self._collapsed_group_label: str = ""
        self._collapsed_sub_item_icon: str = "DecreaseIndentArrowMirrored"
        self._sub_item_label_start: str = "•"

    def toggle_state(self):
        """Toggle the flag variable each time collapse button is clicked"""
        self.collapsed = not self.collapsed

    def get_item(self, name: str) -> Optional[SideMenuItem]:
        """Returns SideMenuItem based on its name"""
        if self.items and len(self.items) > 0:
            for item in self.items:
                if item.name == name:
                    return item
                if len(item.sub_items) > 0:  # Search in subitems
                    for subitem in item.sub_items:
                        if subitem.name == name:
                            return subitem
        return None
    
    def get_root_item(self, name: str) -> Optional[SideMenuItem]:
        """Returns root SideMenuItem based on subitem's name"""
        if self.items and len(self.items) > 0:
            for item in self.items:
                if len(item.sub_items) > 0:  # Search in subitems
                    for subitem in item.sub_items:
                        if subitem.name == name:
                            return item
        return None
    
    def enable_subitems(self, name:Optional[str] = None):
        """Enable rendering all subitems"""
        if name:  # Only enable rendering subitems of the item passed
            item = self.get_item(name)
            if len(item.sub_items) > 0:
                for subitem in item.sub_items:
                    subitem.render = True
            return
        
        if self.items and len(self.items) > 0:  # Enable rendering all the subitems
            for item in self.items:
                if len(item.sub_items) > 0:
                    for subitem in item.sub_items:
                        subitem.render = True

    def disable_subitems(self, name:Optional[str] = None):
        """Disable rendering all subitems"""
        if name:  # Only disable rendering subitems of the item passed
            item = self.get_item(name)
            if len(item.sub_items) > 0:
                for subitem in item.sub_items:
                    subitem.render = False
            return
        
        if self.items and len(self.items) > 0:  # Disable rendering all the subitems
            for item in self.items:
                if len(item.sub_items) > 0:
                    for subitem in item.sub_items:
                        subitem.render = False
    
    @property
    def layout(self) -> Zone:
        """Return layout based on the width"""
        return ui.zone("sidebar", direction=ui.ZoneDirection.COLUMN, size=self.width)

    @property
    def auto_width(self) -> bool:
        return self._auto_width

    @property
    def min_width(self) -> int:
        return self._min_width

    @property
    def max_width(self) -> int:
        return self._max_width

    @property
    def width(self) -> str:
        if self.auto_width and not self.collapsed:
            # Calculating the width based on the longest item label
            label_lengths = []
            for item in self.items:
                if item.render:
                    label_lengths.append(len(item.label))
                    # Adding 2 for sub_item.label due to " " and "•"
                    label_lengths += [
                        len(sub_item.label) + 2 for sub_item in item.sub_items if sub_item.render
                    ]

            if len(label_lengths) > 0:
                width = np.clip(200 + max(label_lengths), self.min_width, self.max_width)
                return f"{width}px"
        return self._width[self.collapsed]

    @width.setter
    def width(self, value: List[str]):
        self._width = value

    @property
    def height(self) -> str:
        return self._height

    @height.setter
    def height(self, value: str):
        self._height = value

    @property
    def documentation_icon(self) -> str:
        return self._documentation_icon

    @property
    def documentation_label(self) -> str:
        return self._documentation_label

    @property
    def collapse_button_icon(self) -> str:
        return self._collapse_button_icon[self.collapsed]

    @collapse_button_icon.setter
    def collapse_button_icon(self, value: List[str]):
        self._collapse_button_icon = value

    @property
    def collapsed_item_label(self) -> str:
        return self._collapsed_item_label

    @collapsed_item_label.setter
    def collapsed_item_label(self, value: str):
        self._collapsed_item_label = value

    @property
    def collapsed_group_label(self) -> str:
        return self._collapsed_group_label

    @collapsed_group_label.setter
    def collapsed_group_label(self, value: str):
        self._collapsed_group_label = value

    @property
    def collapsed_sub_item_icon(self) -> str:
        return self._collapsed_sub_item_icon

    @collapsed_sub_item_icon.setter
    def collapsed_sub_item_icon(self, value: str):
        self._collapsed_sub_item_icon = value

    @property
    def sub_item_label_start(self) -> str:
        return self._sub_item_label_start

    @sub_item_label_start.setter
    def sub_item_label_start(self, value: str):
        self._sub_item_label_start = value

    def groups(self):
        groups = []
        for item in self.items:
            if item.group not in groups:
                groups.append(item.group)
        return groups

    def group_items(self, group):
        group_items = []
        for item in self.items:
            if item.group == group:
                group_items.append(item)
        return group_items

    def get_label(self, item: SideMenuItem):
        return self.collapsed_item_label if self.collapsed else item.label

    def get_icon(
        self,
        item: SideMenuItem,
    ):
        if self.collapsed:
            # Always render original icon when menu is collapsed
            return item.icon
        if self.active_root_item and (item.name == self.active_root_item.name) and (self.expand_root_item or item.expand_always):
            # Render expanded icon when the item is expanded
            return item.expanded_icon
        return item.icon

    def get_sub_label(self, item: SideMenuItem):
        return f" {self.sub_item_label_start} {item.label}"

    def get_sub_icon(self, item: SideMenuItem):
        return self.collapsed_sub_item_icon if self.collapsed else item.icon

    def render_group_items(
        self,
        group: str,
    ):
        """For display purposes, returns new items based on the state of collapsed and active_item_label"""
        group_items = []
        for item in self.items:
            if item.group == group:
                if item.render:
                    group_items.append(
                        SideMenuItem(
                            group=item.group,
                            name=item.name,
                            label=self.get_label(item),
                            icon=self.get_icon(
                                item,
                            ),
                            disabled=item.disabled,
                        )
                    )

                for sub_item in item.sub_items:
                    if sub_item.render:
                        group_items.append(
                            SideMenuItem(
                                group=sub_item.group,
                                name=sub_item.name,
                                label=self.get_sub_label(sub_item),
                                icon=self.get_sub_icon(sub_item),
                                disabled=sub_item.disabled,
                            )
                        )
        return group_items

    def get_nav_content(
        self,
        q: Q,
    ):
        """Returns wave navigation content based on the items and the active index"""
        contents = [
            ui.nav_group(
                label=self.collapsed_group_label,
                items=[
                    ui.nav_item(
                        name=item.name,
                        label=item.label,
                        icon=item.icon,
                        disabled=item.disabled,
                    )
                    for item in self.render_group_items(
                        group=group,
                    )
                ],
            )
            for group in self.groups()
        ]

        if self.documentation:
            # Add documentation item into the last group of items
            contents[-1].items.append(
                ui.nav_item(
                    name="mv_documentation",
                    label=self.documentation_label,
                    icon=self.documentation_icon,
                )
            )

        if self.collapsable:
            # Add collapse item into a new group of items to place it as the last item in the menu
            contents = contents + [
                ui.nav_group(
                    "",
                    items=[
                        ui.nav_item(
                            name="side_menu_toggle_collapse",
                            label="",
                            icon=self.collapse_button_icon,
                        )
                    ],
                )
            ]
        return contents

    def update_zone_layout(self, q: Q):
        pass
        # q.page["meta"].layouts = update_app_layouts(self.layout)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

