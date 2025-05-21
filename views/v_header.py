from itertools import chain

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from controllers import cont_header, db_connection, service_controller


# кнопки навбара
def render_navbar_buttons(collapsed=False):
    navbar_items_dict = cont_header.get_header_links(conn=db_connection.get_conn())
    return [
        dmc.Menu(
            [
                dmc.MenuTarget(
                    dmc.Button(
                        dmc.Text(header_group["header_group_name"], fw=400),
                        variant="subtle",
                        rightSection=DashIconify(icon="gridicons:dropdown", width=20),
                        size="compact-sm",
                    )
                    if not collapsed
                    else dmc.NavLink(
                        label=header_group["header_group_name"],
                        leftSection=DashIconify(icon="tabler-chevron-left"),
                    )
                ),
                dmc.MenuDropdown(
                    list(  # nested list for simple list
                        chain(
                            *[
                                [
                                    dmc.MenuLabel(key),
                                ]  # header
                                + [
                                    dmc.MenuItem(
                                        data["link_name"],
                                        href=data["link_href"],
                                    )
                                    for data in header_group["header_group_content"][
                                        key
                                    ]  # data inside dict
                                ]
                                + [
                                    dmc.MenuDivider(),
                                ]
                                for key in header_group["header_group_content"].keys()
                            ]
                        )
                    )[:-1]
                ),
            ],
            trigger="hover",
            position="bottom" if not collapsed else "left-start",
            withArrow=True
        )
        for header_group in navbar_items_dict
    ]


def get_search_bar(search_target="/search", from_video=False):
    """

    :param search_target:
    :param from_video:
    :return:
    """
    search_placeholder = "Поисковый запрос" if not from_video else "Поиск по видео"
    return html.Form(
        children=[
            dmc.TextInput(
                name="query",
                placeholder=search_placeholder,
                rightSection=[
                    service_controller.dmc_button_from_html("Поиск", height="100%")
                ],
                rightSectionWidth="max-content",
                required=True,
                miw="300px",
            ),
            dmc.TextInput(display="none", value="y", name="l"),
            dmc.TextInput(display="none", value="y", name="auto_search"),
        ],
        method="GET",
        action=search_target,
        className="nav-item",
    )


def render_navbar(from_video=False, from_search=False):

    if from_video:
        search_target = "/players/video/search"
    else:
        search_target = "/search"

    # независимые компоненты
    navbar_brand = html.A(
        dmc.Title("MediaServer", order=3),
        href="/",
        style={
            "textDecoration": "none",
            "height": "min-content",
            "color": "var(--mantine-color-text)",
        },
    )

    navbar_user_dropdown = dmc.Menu(
        [
            dmc.MenuTarget(
                dmc.ActionIcon(
                    DashIconify(icon="mdi:account", width=25),
                    variant="subtle",
                    size="lg",
                )
            ),
            dmc.MenuDropdown(
                [
                    dmc.MenuItem(
                        "Личный кабинет",
                        href="/account",
                    ),
                    dmc.MenuItem(
                        "Выйти",
                        href="/logout",
                    ),
                ],
                p="sm",
            ),
        ],
        trigger="hover",
    )

    mobile_search_bar = dmc.Menu(
        [
            dmc.MenuTarget(
                dmc.ActionIcon(
                    DashIconify(
                        icon="material-symbols:search",
                        width=25,
                    ),
                    variant="subtle",
                    size="lg",
                )
            ),
            dmc.MenuDropdown(
                dmc.Group(
                    get_search_bar(
                        search_target=search_target,
                        from_video=from_video,
                    ),
                    gap="xs",
                ),
                p="sm",
            ),
        ],
        trigger="hover",
    )

    navbar_buttons_collapsed = dmc.Box(
        dmc.Menu(
            [
                dmc.MenuTarget(
                    dmc.ActionIcon(
                        DashIconify(icon="ic:baseline-apps", width=25),
                        variant="subtle",
                        size="lg",
                    )
                ),
                dmc.MenuDropdown(
                    dmc.Stack(render_navbar_buttons(collapsed=True), gap=0)
                ),
            ],
            trigger="hover",
        ),
        ms="auto",
    )

    return dmc.Box(
        [
            dmc.Grid(
                [
                    dmc.GridCol(None, span=1),
                    dmc.GridCol(
                        navbar_brand,
                        span="content",
                        className="justify-content-center align-items-center",
                        display="flex",
                    ),
                    dmc.GridCol(
                        dmc.Group(render_navbar_buttons(), m="auto"),
                        span="auto",
                        h="max-content",
                        display={"base": "none", "xl": "flex"},
                        className="justify-content-center align-items-center",
                    ),
                    dmc.GridCol(
                        None, span="auto", display={"base": "block", "xl": "none"}
                    ),
                    dmc.GridCol(
                        navbar_buttons_collapsed,
                        span="auto",
                        display={"base": "flex", "xl": "none"},
                    ),
                    dmc.GridCol(
                        get_search_bar(
                            search_target=search_target, from_video=from_video
                        ),
                        span="content",
                    ),
                    dmc.GridCol(
                        dmc.Group([navbar_user_dropdown]),
                        span="content",
                    ),
                    dmc.GridCol(None, span=1),
                ],
                w="100%",
                style={"flex-wrap": "nowrap"},
                align="center",
                display={"base": "none", "md": "flex"},
            ),
            dmc.Grid(
                [
                    dmc.GridCol(None, span=1, display={"base": "none", "xs": "block"}),
                    dmc.GridCol(
                        navbar_brand,
                        span="content",
                        className="justify-content-center align-items-center",
                        display="flex",
                    ),
                    dmc.GridCol(
                        span="auto",
                    ),
                    dmc.GridCol(
                        dmc.Group(
                            [
                                dmc.Box(
                                    mobile_search_bar,
                                    ms="auto",
                                ),
                                navbar_user_dropdown,
                                navbar_buttons_collapsed,
                            ]
                        ),
                        span="content",
                    ),
                    dmc.GridCol(None, span=1, display={"base": "none", "xs": "block"}),
                ],
                w="100%",
                style={"flex-wrap": "nowrap"},
                align="center",
                display={"base": "flex", "md": "none"},
            ),
        ],
        w="100%",
    )
