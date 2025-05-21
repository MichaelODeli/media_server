import re
from datetime import datetime

import dash_mantine_components as dmc
import qbittorrentapi
from dash import dcc, html

from controllers import db_connection, file_manager


def add_torrent_modal():
    """

    :return:
    """
    return dmc.Modal(
        title=dmc.Title("Добавить торрент", order=4),
        id="modal-add-torrent",
        centered=True,
        size="55%",
        zIndex=50,
        children=[
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
                        # multiple=True,
                        max_size=40960,
                    ),
                    dmc.TextInput(
                        label="Либо введите magnet-ссылку",
                        w="100%",
                        id="torrent-magnet",
                    ),
                    dmc.Button("Скачать по magnet-ссылке", id="torrent-magnet-btn"),
                    dmc.Stack(id="torrent-upload-props", gap="xs"),
                ]
            )
        ],
    )


def bytes2human(n, formatting="%(value).1f %(symbol)s", symbols="customary"):
    """
    Convert n bytes into a human readable string based on format.
    symbols can be either "customary", "customary_ext", "iec" or "iec_ext",
    see: http://goo.gl/kTQMs

      >>> bytes2human(0)
      '0.0 B'
      >>> bytes2human(0.9)
      '0.0 B'
      >>> bytes2human(1)
      '1.0 B'
      >>> bytes2human(1.9)
      '1.0 B'
      >>> bytes2human(1024)
      '1.0 K'
      >>> bytes2human(1048576)
      '1.0 M'
      >>> bytes2human(1099511627776127398123789121)
      '909.5 Y'

      >>> bytes2human(9856, symbols="customary")
      '9.6 K'
      >>> bytes2human(9856, symbols="customary_ext")
      '9.6 kilo'
      >>> bytes2human(9856, symbols="iec")
      '9.6 Ki'
      >>> bytes2human(9856, symbols="iec_ext")
      '9.6 kibi'

      >>> bytes2human(10000, "%(value).1f %(symbol)s/sec")
      '9.8 K/sec'

      >>> # precision can be adjusted by playing with %f operator
      >>> bytes2human(10000, format="%(value).5f %(symbol)s")
      '9.76562 K'
    """
    symbols_dict = {
        "customary": ("B", "Kb", "Mb", "Gb", "Tb", "Pb", "Eb", "Zb", "Yb"),
        "customary_ext": (
            "byte",
            "kilo",
            "mega",
            "giga",
            "tera",
            "peta",
            "exa",
            "zetta",
            "iotta",
        ),
        "iec": ("Bi", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi", "Yi"),
        "iec_ext": (
            "byte",
            "kibi",
            "mebi",
            "gibi",
            "tebi",
            "pebi",
            "exbi",
            "zebi",
            "yobi",
        ),
    }
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = symbols_dict[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)


def decode_torrent_status(name):
    """

    :param name:
    :return:
    """
    status_dict = {
        "error": "Ошибка",
        "missingFiles": "Нет файлов",
        "uploading": "[↑] Раздача",
        "pausedUP": "[↑] Пауза",
        "queuedUP": "[↑] В очереди",
        "stalledUP": "[↑] Ожидание",
        "checkingUP": "[↑] Проверка",
        "forcedUP": "[П] Раздача",
        "allocating": "[↓] Выделение места",
        "downloading": "[↓] Загрузка",
        "metaDL": "[↓] Проверка мета",
        "pausedDL": "[↓] Пауза",
        "queuedDL": "[↓] В очереди",
        "stalledDL": "[↓] Ожидание",
        "checkingDL": "[↓] Проверка",
        "forcedDL": "[П] Загрузка",
        "checkingResumeData": "[↓] Проверка",
        "moving": "Перемещение",
    }

    if name in status_dict.keys():
        return status_dict[name]
    else:
        return "Неизвестно"


def verify_magnet_link(magnet_link):
    """

    :param magnet_link:
    :return:
    """
    pattern = re.compile(r"magnet:\?xt=urn:[a-z0-9]+:[a-zA-Z0-9]{32}")
    result = pattern.match(magnet_link)
    if result is not None:
        return True
    else:
        return False


def get_torrents_data_dict(source_page):
    """

    :param source_page:
    :return:
    """
    conn = db_connection.get_conn()
    settings = file_manager.get_settings(conn)

    qbt_ip = settings["apps.torrents.qbittorrent_ip"]
    qbt_port = settings["apps.torrents.qbittorrent_port"]
    qbt_login = settings["apps.torrents.qbittorrent_login"]
    qbt_password = settings["apps.torrents.qbittorrent_password"]

    qbt_client = qbittorrentapi.Client(
        host=f"{qbt_ip}:{qbt_port}", username=qbt_login, password=qbt_password
    )

    if source_page == "main_page":
        return {
            "all": len(qbt_client.torrents_info()),
            "uploading": len(qbt_client.torrents_info(status_filter="seeding")),
            "downloading": len(
                qbt_client.torrents_info(status_filter="downloading")
            ),
        }
    elif source_page == "torrents_page":
        return [
            {
                "hash": torrent_info["hash"],
                "name": torrent_info["name"],
                "progress": int(torrent_info["progress"] * 100),
                "status": decode_torrent_status(torrent_info["state"]),
                "seeds": torrent_info["num_seeds"],
                "download_speed": bytes2human(torrent_info["dlspeed"]) + "/s",
                "upload_speed": bytes2human(torrent_info["upspeed"]) + "/s",
                "added": datetime.fromtimestamp(torrent_info["added_on"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "completed": (
                    datetime.fromtimestamp(torrent_info["completion_on"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if torrent_info["completion_on"] > 0
                    else ""
                ),
            }
            for torrent_info in qbt_client.torrents_info()
        ]
    else:
        return ValueError("Некорректная страница.")


def get_torrents_table_data(source_page="torrents_page"):
    """

    :param source_page:
    :return:
    """
    return [
        [
            dmc.Checkbox(
                id={"type": "torrent-checkboxes", "id": torrent_dict["hash"]},
                checked=False,
            ),
            torrent_dict["name"],
            dmc.ProgressRoot(
                [
                    dmc.ProgressSection(
                        dmc.ProgressLabel(f"{str(torrent_dict['progress'])}%"),
                        value=torrent_dict["progress"],
                    ),
                ],
                size="xl",
            ),
            torrent_dict["status"],
            torrent_dict["seeds"],
            torrent_dict["download_speed"],
            torrent_dict["upload_speed"],
            torrent_dict["added"],
            torrent_dict["completed"],
        ]
        for torrent_dict in get_torrents_data_dict(source_page=source_page)
    ]
