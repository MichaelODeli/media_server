import dash_mantine_components as dmc
from dash import (ALL, Input, Output, State, callback, register_page)
from dash_iconify import DashIconify

register_page(__name__, path="/budget/subscriptions", icon="fa-solid:home")


def layout(l="n", **kwargs):  # noqa: E741
    """

    :param l:
    :param kwargs:
    :return:
    """
    if l == "n":
        return dmc.Container()
    else:
        add_sub_modal = dmc.Modal(
            title=dmc.Title("Добавить подписку", order=3),
            id="modal-add-sub",
            zIndex=10000,
            children=[
                dmc.Text("I am in a modal component."),
            ],
        )

        remove_sub_confirm_modal = dmc.Modal(
            title=dmc.Title("Подтверждение", order=3),
            id="modal-remove-confirm-sub",
            zIndex=10000,
            children=[
                dmc.Text("Вы действительно хотите удалить подписку {sub_name}?"),
            ],
        )

        properties_sub_modal = dmc.Modal(
            title=dmc.Title("Настройка подписки {sub_name}", order=3),
            id="modal-sub-properties",
            zIndex=10000,
            children=[
                dmc.Text("Какие-то настройки"),
            ],
        )

        sub_icon = DashIconify(icon="ri:vk-fill", height=40)
        sub_container = dmc.Card(
            dmc.Stack(
                [
                    dmc.Group(
                        [
                            sub_icon,
                            dmc.Title("ВК Музыка", order=3, className="h-content"),
                        ],
                        align="center",
                        gap="xs",
                    ),
                    dmc.Space(),
                    dmc.Text("Истекает через 250 дней"),
                    dmc.Progress(value=250 / 365 * 100),
                    dmc.Space(),
                    dmc.Group(
                        [
                            dmc.Title(
                                dmc.NumberFormatter(
                                    value=2500, prefix="₽", thousandSeparator=True
                                ),
                                order=3,
                            ),
                            dmc.Title("/", order=3),
                            dmc.Title("год", order=3),
                            dmc.Flex(
                                [
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:delete-outline"
                                        ),
                                        mx=5,
                                        color="red",
                                        id={"type": "sub-remove", "id": 1}
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:settings-outline"
                                        ),
                                        mx=5,
                                        id={"type": "sub-setting", "id": 1}
                                    ),
                                ],
                                w="100%",
                                direction="row-reverse",
                            ),
                        ],
                        wrap="nowrap",
                        align="flex-end",
                        gap="xs",
                    ),
                ],
                gap="sm",
            ),
            bg="var(--mantine-primary-color-light)",
            w={"base": "100%", "sm": "300px"},
            my="xs",
        )

        subs_container = dmc.Flex(
            direction="row",
            wrap="wrap",
            justify="space-around",
            children=[sub_container] * 12,
        )

        subs_header = dmc.Grid(
            [
                dmc.GridCol(
                    dmc.Title("Менеджер подписок", order=3, className="h-content"),
                    span="content",
                ),
                dmc.GridCol(span="auto"),
                dmc.GridCol(
                    span="content",
                    children=[
                        dmc.Group(
                            [
                                dmc.ActionIcon(
                                    DashIconify(icon="mdi:plus", height=25),
                                    color="green",
                                    size="lg",
                                    id="add-sub",
                                ),
                                dmc.Menu(
                                    [
                                        dmc.MenuTarget(
                                            dmc.ActionIcon(
                                                DashIconify(icon="mdi:sort", height=25),
                                                size="lg",
                                            )
                                        ),
                                        dmc.MenuDropdown(
                                            [
                                                dmc.MenuItem(
                                                    "По дате истечения",
                                                    leftSection=DashIconify(
                                                        icon="mdi:sort-clock-ascending",
                                                        height=20,
                                                    ),
                                                ),
                                                dmc.MenuItem(
                                                    "По дате истечения",
                                                    leftSection=DashIconify(
                                                        icon="mdi:sort-clock-descending",
                                                        height=20,
                                                    ),
                                                ),
                                                dmc.MenuItem(
                                                    "По стоимости",
                                                    leftSection=DashIconify(
                                                        icon="mdi:sort-numeric-ascending",
                                                        height=20,
                                                    ),
                                                ),
                                                dmc.MenuItem(
                                                    "По стоимости",
                                                    leftSection=DashIconify(
                                                        icon="mdi:sort-numeric-descending",
                                                        height=20,
                                                    ),
                                                ),
                                            ]
                                        ),
                                    ],
                                    trigger="hover",
                                ),
                            ],
                            gap="xs",
                        )
                    ],
                ),
            ]
        )

        return dmc.Stack(
            [subs_header, subs_container, add_sub_modal, remove_sub_confirm_modal, properties_sub_modal],
            # w="98%",
            pt=10,
            mt=20,
            mx="md",
        )


@callback(
    Output("modal-add-sub", "opened"),
    Input("add-sub", "n_clicks"),
    State("modal-add-sub", "opened"),
    prevent_initial_call=True,
)
def modal_add_sub(nc1, opened):
    """

    :param nc1:
    :param opened:
    :return:
    """
    return not opened


@callback(
    Output("modal-sub-properties", "opened"),
    Input({"type": "sub-setting", "id": ALL}, "n_clicks"),
    State("modal-sub-properties", "opened"),
    prevent_initial_call=True,
)
def modal_edit_sub(nc1, opened):
    """

    :param nc1:
    :param opened:
    :return:
    """
    return not opened


@callback(
    Output("modal-remove-confirm-sub", "opened"),
    Input({"type": "sub-remove", "id": ALL}, "n_clicks"),
    State("modal-remove-confirm-sub", "opened"),
    prevent_initial_call=True,
)
def modal_remove_sub(nc1, opened):
    """

    :param nc1:
    :param opened:
    :return:
    """
    return not opened
