import dash_mantine_components as dmc
from dash import (register_page)
from dash_iconify import DashIconify

from views import v_calendar

register_page(__name__, path="/calendar", icon="fa-solid:home")


def layout(l="n", **kwargs):  # noqa: E741
    """

    :param l:
    :param kwargs:
    :return:
    """
    if l == "n":
        return dmc.Container()
    else:

        return dmc.AppShell(
            [
                dmc.AppShellNavbar(
                    dmc.Stack(
                        [
                            v_calendar.render_mini_calendar(),
                            dmc.Divider(),
                            dmc.Title("Ближайшие задачи", order=3, ps="xs"),
                            v_calendar.render_plans_navbar(),
                        ],
                        h="100%",
                        pt="xs",
                    ),
                    # className="border-end-0",
                ),
                dmc.AppShellMain(
                    dmc.Stack(
                        [
                            dmc.Group(
                                [
                                    dmc.ActionIcon(
                                        DashIconify(icon="ic:baseline-arrow-back-ios-new", height=25),
                                        variant='light'
                                    ),
                                    dmc.Title("Сентябрь 2024", order=3),
                                    dmc.ActionIcon(
                                        DashIconify(icon="ic:baseline-arrow-forward-ios", height=25),
                                        variant='light'
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(icon="ic:sharp-plus", height=25),
                                        color="green.8",
                                        variant='light',
                                        ms='auto',
                                        size='lg'
                                    ),
                                ]
                            ),
                            v_calendar.render_maxi_calendar(),
                        ],
                        mah="95%",
                        h="95%",
                        gap="xs",
                    ),
                    h="calc(100dvh - var(--app-shell-header-height) - 40px) !important",
                    mih="calc(100dvh - var(--app-shell-header-height) - 40px) !important",
                    style={"overflow": "hidden"},
                    px='sm',
                    pt='.25rem'
                ),
            ],
            navbar={
                "width": 300,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
        )
