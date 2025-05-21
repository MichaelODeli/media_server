import dash_mantine_components as dmc
from dash import (ALL, Input, Output, State, callback, dcc, html, no_update, register_page)
from dash_iconify import DashIconify
from flask import request

from controllers import cont_files as cont_f
from controllers import cont_torrents as cont_t
from controllers import db_connection, file_manager
from controllers import service_controller as service

register_page(__name__, path="/torrents", icon="fa-solid:home")

conn = db_connection.get_conn()
settings = file_manager.get_settings(conn)
qbt_ip = settings["apps.torrents.qbittorrent_ip"]
qbt_port = settings["apps.torrents.qbittorrent_port"]
qbt_link = f"http://{qbt_ip}:{qbt_port}"


def layout(l="n", **kwargs):  # noqa: E741
    """

    :param l:
    :param kwargs:
    :return:
    """
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        service.log_printer(request.remote_addr, "torrents", "page opened")

        # all workers must be here!
        return dmc.Container(
            children=[
                # dcc.Location(id='torrent-link', title='_blank', href='#'),
                html.Div(
                    [
                        dmc.Card(
                            [
                                dmc.Grid(
                                    [
                                        dmc.GridCol(
                                            dmc.Title(
                                                "Управление торрентами",
                                                style={"margin": "0"},
                                                order=4,
                                            ),
                                            span="content",
                                        ),
                                        dmc.GridCol(span="auto"),
                                        dmc.Group(
                                            [
                                                service.get_button_with_icon(
                                                    button_icon="material-symbols:sync",
                                                    button_title="Обновить список",
                                                    button_id="torrent-update",
                                                ),
                                                service.get_button_with_icon(
                                                    button_icon="material-symbols:add",
                                                    button_title="Добавить торрент",
                                                    button_id="torrent-add",
                                                ),
                                                service.get_button_with_icon(
                                                    button_icon="material-symbols:play-pause",
                                                    button_title="Запустить/остановить торрент",
                                                    button_id="torrent-startstop",
                                                    disabled=True,
                                                ),
                                                service.get_button_with_icon(
                                                    button_icon="material-symbols:info-outline",
                                                    button_title="Информация о торренте",
                                                    button_id="torrent-info",
                                                    disabled=True,
                                                ),
                                                service.get_button_with_icon(
                                                    button_icon="material-symbols:delete",
                                                    button_title="Удалить торрент",
                                                    button_id="torrent-delete",
                                                    color="red",
                                                    disabled=True,
                                                ),
                                                dmc.Anchor(
                                                    dmc.Button(
                                                        "Открыть qbittorrent",
                                                        rightSection=DashIconify(
                                                            icon="mdi:external-link"
                                                        ),
                                                    ),
                                                    href=qbt_link,
                                                    target="_blank",
                                                ),
                                            ],
                                            style={"margin": "5px"},
                                            gap="xs",
                                            id="dummy-4",
                                        ),
                                    ],
                                    align="stretch",
                                    justify="center",
                                ),
                                dmc.Space(h=15),
                                html.Div(id="torrents-table-container"),
                            ],
                            # className="block-background",
                            shadow="md",
                        ),
                        dmc.Modal(
                            title=dmc.Title("Добавить торрент", order=5),
                            id="modal-add-torrent",
                            centered=True,
                            size="55%",
                            zIndex=50,
                        ),
                        html.Div(id="torrent-notifications-container"),
                    ],
                ),
            ],
            pt=20,
            # style={"paddingTop": 20},
            # className="dmc-container",
            miw="90%",
        )


@callback(
    Output("modal-add-torrent", "opened", allow_duplicate=True),
    Output("modal-add-torrent", "children"),
    Input("torrent-add", "n_clicks"),
    State("modal-add-torrent", "opened"),
    prevent_initial_call=True,
)
def toggle_torrent_modal(nc1, opened):
    """

    :param nc1:
    :param opened:
    :return:
    """
    modal_children = [
        dmc.Stack(
            [
                dcc.Upload(
                    id="upload-torrent",
                    accept=".torrent",
                    children=html.Div(
                        [
                            "Перетащите или ",
                            html.A(
                                "выберите файлы",
                                className="link-opacity-100",
                                href="#",
                            ),
                        ],
                    ),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        # "margin": "10px",
                    },
                    # Allow multiple files to be uploaded
                    multiple=True,
                ),
                dmc.TextInput(
                    label="Или введите magnet-ссылку", w="100%", id="torrent-magnet"
                ),
                dmc.Button("Скачать по magnet-ссылке", id="torrent-magnet-btn"),
                dmc.Stack(
                    id="torrent-upload-props",
                    children=html.Div(id="torrent-start-download"),
                ),
            ]
        )
    ]
    return not opened, modal_children


@callback(
    Output("modal-add-torrent", "opened"),
    Output("torrent-upload-props", "children"),
    Output("upload-torrent", "disabled"),
    Output("torrent-magnet-btn", "disabled"),
    Output("torrent-magnet", "disabled"),
    Output("torrent-magnet", "error"),
    Input("upload-torrent", "contents"),
    Input("torrent-magnet-btn", "n_clicks"),
    Input("torrent-start-download", "n_clicks"),
    State("upload-torrent", "filename"),
    State("torrent-magnet", "value"),
    prevent_initial_call=True,
)
def parce_torrent_file(
    file_content, n_clicks_magnet, n_clicks_start, file_name, magnet_link=None
):
    """

    :param file_content:
    :param n_clicks_magnet:
    :param n_clicks_start:
    :param file_name:
    :param magnet_link:
    :return:
    """
    dis_upload = True
    dis_magnet_btn = True
    dis_magnet_input = True

    # check link and file
    if n_clicks_magnet is not None and magnet_link != "" and magnet_link is not None:
        prop_source = "magnet"
        if cont_t.verify_magnet_link(magnet_link):
            magnet_link = magnet_link
        else:
            return [no_update] * 5 + ["Неверная ссылка"]
    elif file_content is not None:
        prop_source = "file"
        # for torrent_file in file_content:
        #     torrent_bytes = base64.b64decode(torrent_file.split(",")[1])
    else:
        return [no_update] * 6

    # add properties of file/url
    properties = [
        dmc.Title("Информация", order=5),
        dmc.Stack(
            gap="xs",
            children=[
                dmc.Text(
                    f"Для загрузки выбрано {len(file_name)} торрент-файла(ов)."
                    if magnet_link is None or magnet_link == ""
                    else "Для загрузки используется magnet-ссылка."
                ),
            ],
        ),
        dmc.Space(h=7),
        dmc.Title("Выберите категорию загружаемого файла", order=5),
        dmc.Select(
            placeholder="Выберите",
            id="torrent-category-select",
            value="other",
            data=[
                # value - link with temp-download folder and category, label - category name
                {"value": "films", "label": "Фильмы"},
                {"value": "apps", "label": "Программы"},
                {"value": "serials", "label": "Сериалы"},
                {"value": "other", "label": "Другое"},
            ],
            style={"width": "100%", "margin": "auto"},
        ),
        dmc.Button("Начать загрузку", id="torrent-start-download", disabled=True),
    ]

    # if not download - return properties
    if n_clicks_start is None:
        return (
            no_update,
            properties,
            dis_upload,
            dis_magnet_btn,
            dis_magnet_input,
            False,
        )
    else:
        print("trigger download")
        if prop_source == "magnet":
            print("use magnet")
            # qbt_client.torrents_add(urls=magnet_link)
        elif prop_source == "file":
            print("use file")
            # qbt_client.torrents_add(torrent_files=torrent_bytes)
        else:
            print("unknown")

        return [False] + [no_update] * 5


@callback(
    Output("torrents-table-container", "children"), Input("torrent-update", "n_clicks")
)
def return_torrents_data(n):
    """

    :param n:
    :return:
    """
    service.log_printer(request.remote_addr, "torrents", "toggle update")

    datatable = cont_t.get_torrents_table_data()
    # datatable = None
    return (
        cont_f.generate_html_table(
            header=[
                "",
                "Название файла",
                "Прогресс",
                "Статус",
                "Сиды",
                "Скорость загрузки",
                "Скорость отдачи",
                "Добавлен",
                "Завершен",
            ],
            data=datatable,
            align="center",
            variant="compact",
            striped=True,
            highlight_on_hover=True,
        )
        if datatable is not None
        else dmc.Title(
            "Ошибка получения данных", style={"text-align": "center"}, order=4
        )
    )


@callback(
    Output("torrents-table-container", "style"),
    Input({"type": "torrent-checkboxes", "id": ALL}, "checked"),
    State({"type": "torrent-checkboxes", "id": ALL}, "id"),
    prevent_initial_call=True,
)
def test(checkboxes_input, checkboxes_ids):
    if [False] * len(checkboxes_input) == checkboxes_input:
        return no_update
    else:
        torrent_ids = []
        for prop_id, checked in zip(checkboxes_ids, checkboxes_input):
            if checked:
                torrent_ids.append(prop_id["id"])

        print(torrent_ids)
        return no_update
