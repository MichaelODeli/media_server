import dash_mantine_components as dmc
import psutil
from dash import Input, Output, callback, clientside_callback, html, register_page
from dash_iconify import DashIconify
from flask import request

from controllers import cont_settings, db_connection, file_manager
from controllers import service_controller as service

register_page(__name__, path="/settings", icon="fa-solid:home")


def layout(l="n", tab="server_info", **kwargs):  # noqa: E741
    """

    :param l:
    :param tab:
    :param kwargs:
    :return:
    """
    if l == "n":
        return dmc.Container()
    service.log_printer(request.remote_addr, "settings", "page opened")

    return dmc.Container(
        children=[
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab(
                                dmc.Title("Основные настройки", order=5), value="main"
                            ),
                            dmc.TabsTab(
                                dmc.Title("Менеджер файлов", order=5), value="files"
                            ),
                            dmc.TabsTab(
                                dmc.Title("Настройка виджетов и приложений", order=5),
                                value="widgets",
                            ),
                            dmc.TabsTab(
                                dmc.Title("Свойства системы", order=5),
                                value="server_info",
                            ),
                        ],
                        grow=True,
                    ),
                ],
                variant="outline",
                orientation="horizontal",
                style={"height": "100%", "width": "100%"},
                value=tab,
                id="tabs-settings",
            ),
            html.Div(id="tabs-content", style={"paddingTop": 10}),
        ],
        pt=10,
        mt=20,
        # style={"paddingTop": 20, 'width': '100%'},
        className="dmc-container block-background",
        w="100%",
    )


@callback(Output("tabs-content", "children"), Input("tabs-settings", "value"))
def render_settings_content(active, test=True):
    """

    :param active:
    :param test:
    :return:
    """
    conn = db_connection.get_conn()
    categories = file_manager.get_categories(conn)
    settings = file_manager.get_settings(conn)

    if active == "files":
        return dmc.Stack(
            [
                dmc.Title("Каталоги", order=4),
                dmc.TextInput(
                    label="Родительский каталог с папками",
                    style={"width": 250},
                    id="settings-catalog-main_folder",
                    value=(
                        settings["filemanager.baseway.test"]
                        if test
                        else settings["filemanager.baseway"]
                    ),
                    disabled=True,
                ),
                dmc.NumberInput(
                    label="Глубина обхода папок",
                    value=int(settings["filemanager.depth"]),
                    min=1,
                    style={"width": 250},
                    id="settings-catalog-depth",
                    disabled=True,
                ),
                dmc.Button("Сохранить", style={"width": "min-content"}, disabled=True),
                dmc.Divider(variant="solid"),
                dmc.Title("Обновление библиотеки", order=4),
                dmc.NumberInput(
                    label="Интервал обновления базы",
                    description="Указана периодичность в днях",
                    value=int(settings["filemanager.update_interval"]),
                    min=1,
                    style={"width": 250},
                    id="settings-catalog-update_interval",
                    disabled=True,
                ),
                dmc.Button("Сохранить", style={"width": "min-content"}, disabled=True),
                dmc.Divider(variant="solid"),
                dmc.Title("Категории", order=4),
                dmc.MultiSelect(
                    label="Используемые категории файлов",
                    description="Категорией служит название подпапки в родительской папке с файлами. Обратите внимание, папки, у которых в начале стоит нижнее подчеркивание, не будут проанализированы.",
                    value=[i["category_name"] for i in categories],
                    data=[i["category_name"] for i in categories],
                    style={"width": 400, "marginBottom": 10},
                    id="settings-catalog-all_categories",
                    disabled=True,
                ),
                dmc.MultiSelect(
                    label="Категории с видеоконтентом",
                    description="Для выбранных категорий будет доступен просмотр видео в браузере",
                    value=[
                        i["category_name"]
                        for i in categories
                        if i["main_mime_type_id"] == 9
                    ],
                    data=[i["category_name"] for i in categories],
                    style={"width": 400, "marginBottom": 10},
                    id="settings-catalog-video_categories",
                    disabled=True,
                ),
                dmc.Group(
                    [
                        dmc.Button(
                            "Сохранить изменения",
                            id="settings-catalog-update_by_categories",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                    ],
                    style={"width": "max-content"},
                ),
                dmc.Divider(variant="solid"),
                dmc.Title("Кнопки управления", order=4),
                dmc.Group(
                    [
                        dmc.Button(
                            "Пересканировать библиотеку файлов",
                            id="settings-catalog-manual_update",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dmc.Button(
                            "Пересканировать типы категорий",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dmc.Button(
                            "Пересканировать категории",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dmc.Button(
                            "Сброс базы файлового менеджера",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dmc.Button(
                            "Отключить файловый менеджер",
                            id="settings-catalog-disable_update",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                    ],
                    gap="xs",
                ),
                dmc.Divider(variant="solid"),
                # dmc.Title("Лог обновления базы", order=4),
                # dmc.Button(
                #     "Получить лог",
                #     id="settings-catalog-get_log",
                #     style={"width": "max-content"},
                # ),
            ]
        )
    elif active == "server_info":
        return [
            dmc.Space(h=5),
            dmc.Table(
                [
                    dmc.TableTbody(
                        cont_settings.get_system_info_rows()
                        + cont_settings.get_cpu_info_rows()
                        + cont_settings.get_ram_swap_info_rows()
                        + cont_settings.get_partitions_info_rows()
                    ),
                ],
                style={"table-layout": "auto", "width": "100%"},
                className="no-box-shadow",
            ),
        ]
    elif active == "widgets":
        return dmc.Stack(
            [
                dmc.Title("Погода", order=4),
                dmc.Switch(
                    label="Включить",
                    checked=bool(settings["apps.weather.enabled"]),
                    disabled=True,
                ),
                dmc.TextInput(
                    label="Город, для которого нужно отображать погоду",
                    style={"width": 250},
                    id="widgets-weather-city",
                    value=settings["apps.weather.city"],
                    disabled=True,
                ),
                dmc.Button(
                    "Сохранить",
                    style={"width": "min-content"},
                    disabled=True,
                ),
                dmc.Divider(variant="solid"),
                dmc.Title("Размеры разделов", order=4),
                # dmc.MultiSelect(
                #     label="Выберите разделы, для которых будут отображаться их размеры на главном экране",
                #     style={"width": 400},
                #     id="widgets-partitions-selected",
                #     disabled=True,
                # ),
                dmc.Switch(
                    label="Включить",
                    checked=bool(settings["apps.drives_monitor.enabled"]),
                    disabled=True,
                ),
                dmc.Button(
                    "Сохранить",
                    style={"width": "min-content"},
                    disabled=True,
                ),
                dmc.Divider(variant="solid"),
                dmc.Title("Системный монитор", order=4),
                dmc.Switch(
                    label="Включить",
                    checked=bool(settings["apps.system_monitor.enabled"]),
                    disabled=True,
                ),
                dmc.Text(
                    "Выберите те параметры, которые будут отображаться на главном экране"
                ),
                dmc.Stack(
                    children=[
                        dmc.Checkbox(
                            label="Загрузка CPU",
                            checked=bool(settings["apps.system_monitor.cpu_monitor"]),
                            disabled=True,
                            m=0,
                        ),
                        dmc.Checkbox(
                            label="Загрузка RAM",
                            checked=bool(settings["apps.system_monitor.ram_monitor"]),
                            disabled=True,
                            m=0,
                        ),
                        dmc.Checkbox(
                            label="Загрузка SWAP",
                            checked=bool(settings["apps.system_monitor.swap_monitor"]),
                            disabled=True,
                            m=0,
                        ),
                        dmc.Checkbox(
                            label="Текущая скорость подключения",
                            checked=bool(settings["apps.system_monitor.network_speed"]),
                            disabled=True,
                            m=0,
                        ),
                        dmc.Button(
                            "Сохранить",
                            style={"width": "min-content"},
                            disabled=True,
                        ),
                    ],
                    mr="auto",
                    align="flex-start",
                ),
                dmc.Divider(variant="solid"),
                dmc.Title("Мониторинг торрентов", order=4),
                dmc.Switch(
                    label="Включить",
                    checked=bool(settings["apps.torrents.enabled"]),
                    disabled=True,
                ),
                dmc.TextInput(
                    label="IP адрес сервера qBittorrent",
                    style={"width": 250},
                    value=settings["apps.torrents.qbittorrent_ip"],
                    disabled=True,
                ),
                dmc.TextInput(
                    label="Порт сервера qBittorrent",
                    style={"width": 250},
                    value=settings["apps.torrents.qbittorrent_port"],
                    disabled=True,
                ),
                dmc.TextInput(
                    label="Логин сервера qBittorrent",
                    style={"width": 250},
                    disabled=True,
                    value=settings["apps.torrents.qbittorrent_login"],
                ),
                dmc.PasswordInput(
                    label="Пароль сервера qBittorrent",
                    style={"width": 250},
                    disabled=True,
                    value=settings["apps.torrents.qbittorrent_password"],
                ),
                dmc.Group(
                    [
                        dmc.Button(
                            "Тест подключения",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dmc.Button(
                            "Сохранить",
                            style={"width": "min-content"},
                            disabled=True,
                        ),
                    ]
                ),
                dmc.Divider(variant="solid"),
            ],
            # w='100%'
        )
    else:
        return [
            dmc.Space(h=5),
            dmc.Stack(
                children=[
                    dmc.Switch(
                        onLabel=DashIconify(icon="radix-icons:moon", width=20),
                        offLabel=DashIconify(icon="radix-icons:sun", width=20),
                        size="lg",
                        # id={"type": "color-mode-switch", "index": random.randint(0, 5)},
                        id="color-mode-switch",
                        className="nav-item",
                        persistence_type="session",
                        persistence=True,
                        label="Переключить тему приложения",
                    )
                ],
            ),
        ]


@callback(
    [
        Output("cpu-ring-usage", "children"),
    ],
    [Input("show-cpu-load", "n_clicks")],
    prevent_initial_call=True,
)
def get_cpu_load_rings(_):
    """

    :param _:
    :return:
    """
    return [
        dmc.Group(
            [
                dmc.RingProgress(
                    sections=[
                        {
                            "value": percentage,
                            "color": "custom-primary-color",
                            "tooltip": f"{percentage}%",
                        },
                    ],
                    label=dmc.Text(
                        f"CPU{i}",
                        c="black",
                        ta="center",
                    ),
                    size=100,
                    roundCaps=True,
                )
                for i, percentage in enumerate(
                    psutil.cpu_percent(percpu=True, interval=0.1)
                )
            ]
        )
    ]


clientside_callback(
    """
    (switchOn) => {
    switchOn = !switchOn
    document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark");
    return window.dash_clientside.no_update
    }
    """,
    Output("dummy-1", "style"),
    Input("color-mode-switch", "checked"),
)


@callback(
    Output("mantine_theme", "forceColorScheme"),
    Input("color-mode-switch", "checked"),
)
def make_mantine_theme(value):
    """

    :param value: color-mode-switch
    :return: mantine_theme.forceColorScheme
    """
    return "dark" if value else "light"
