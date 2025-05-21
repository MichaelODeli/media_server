import calendar
import locale
import shutil
from datetime import datetime, timedelta

import dash_mantine_components as dmc
import psutil
from dash import html
from dash_iconify import DashIconify

from controllers import cont_torrents, db_connection, file_manager
from controllers.cont_torrents import bytes2human
from controllers.cont_settings import get_readable_bytes

locale.setlocale(locale.LC_ALL, "ru_RU")


def get_torrent_status():
    """
    :return List(str):
    """
    try:
        torrents_dict = cont_torrents.get_torrents_data_dict(source_page="main_page")

        count_all = torrents_dict["all"]
        count_downloading = torrents_dict["downloading"]
        count_uploading = torrents_dict["uploading"]

        return (
            f"Активных: {count_all}",
            f"Скачивается: {count_downloading}",
            f"Раздается: {count_uploading}",
        )
    except Exception:
        return ["qbittorrent не отвечает."] * 3


def get_color_by_value(current_value=None, max_value=None, percent=None):
    """

    :param current_value:
    :param max_value:
    :param percent: additional param
    :return (str): color name
    """
    if percent is None:
        percent = (current_value / max_value) * 100
    return (
        "custom-primary-color"
        if percent < 70
        else ("orange" if percent < 90 else "red")
    )


def get_progress(
    drive: str,
    current_value: float,
    max_value: float,
    component_id: str,
    valid: bool,
):
    """
    Получить прогресс-бар с текущим объемом накопителя

    :param drive: название диска/раздела
    :param current_value: текущий занятый объем диска
    :param max_value: максимальная емкость раздела
    :param id: идентификатор блока
    :param valid: наличие раздела. Если нет - то прогресс-бар будет окрашен в красный цвет.
    """

    if valid:
        return html.Tr(
            [
                html.Td(drive, style={"text-wrap": "nowrap"}),
                html.Td(
                    dmc.ProgressRoot(
                        [
                            dmc.ProgressSection(
                                dmc.ProgressLabel(
                                    f"{get_readable_bytes(current_value)} | {get_readable_bytes(max_value)}"
                                ),
                                value=int(round(current_value / max_value, 2) * 100),
                                color=get_color_by_value(current_value, max_value),
                                id=component_id,
                            )
                        ],
                        size="xl",
                    ),
                    style={"width": "100%", "padding": "0 2% 0 2%"},
                ),
            ]
        )
    else:
        return html.Tr(
            [
                html.Td(drive),
                html.Td(
                    dmc.ProgressRoot(
                        [
                            dmc.ProgressSection(
                                dmc.ProgressLabel("Диск не обнаружен"),
                                value=100,
                                color="#cc0000",
                                id=component_id,
                            )
                        ],
                        size="xl",
                    ),
                    style={"width": "100%", "padding": "3%"},
                ),
            ]
        )


def get_drive_size(partition):
    """
    Получить размер диска/раздела в виде кольцевого прогресс-бара.

    :param partition: путь к разделу
    """
    try:
        mountpoint = partition.mountpoint
        total, used, _ = shutil.disk_usage(mountpoint)
        valid = True
    except Exception:
        total = 1
        used = 1
        valid = False
        mountpoint = None

    return get_progress(
        mountpoint, int(used), int(total), f"ring-{mountpoint}", valid=valid
    )


def widget_disk_size(**kwargs):
    """
    Функция создает карточку с информацией о свободном месте на дисках.

    :param **kwargs: любое количество ключевых аргументов.

    :return (dmc.Card): карточка с информацией о свободном месте на дисках.
    """
    return dmc.Card(
        [
            dmc.Text("Свободное место на разделах", size="xl", ta="center"),
            dmc.Space(h=10),
            html.Table([get_drive_size(part) for part in psutil.disk_partitions()]),
            dmc.Space(h=10),
            dmc.Anchor("Подробные свойства", href="/settings?l=y&tab=server_info"),
        ],
        className="mobile-block",
        shadow="md",
        # style={"min-height": "100%"},
    )


def get_weather_label(selected_date: str, temperature: list, weather_type="sunny"):
    """
    Функция создает метку с информацией о погоде.

    :param (str) selected_date: дата в формате DDMMYYYY.
    :param (list) temperature: список с температурой в формате [day_temp, night_temp].
    :param (str) weather_type: тип погоды, по умолчанию "sunny".

    :return (dmc.Stack): метка с информацией о погоде.
    """
    weather_types = {
        "sunny": "material-symbols:sunny",
        "partly-cloudy": "material-symbols:partly-cloudy-day",
        "cloudy": "material-symbols:cloudy",
        "snow": "material-symbols:cloudy-snowing",
        "rain": "material-symbols:rainy",
        "thunderstorm": "material-symbols:thunderstorm",
    }
    if weather_type not in weather_types:
        raise ValueError("Incorrect weather type.")

    converted_date = datetime.strptime(selected_date, "%d%m%Y").date()
    return dmc.Stack(
        [
            dmc.Text(
                calendar.day_abbr[converted_date.weekday()].capitalize(),
                c="custom-primary-color" if converted_date.weekday() < 5 else "red",
            ),
            dmc.Text(
                f"{converted_date.day} {calendar.month_abbr[converted_date.month]}",
                c="gray",
            ),
            dmc.Space(h=10),
            DashIconify(icon=weather_types[weather_type], width=40),
            dmc.Text(temperature[0], c="custom-primary-color"),
            dmc.Text(temperature[1], c="gray"),
        ],
        align="center",
        gap=0,
    )


def get_date_string(plus: int = 0, pattern="%d%m%Y"):
    """
    Вывод сегодняшней даты с опцией добавление определенного числа дней к числу.

    :param (int) plus: кол-во добалвяемых дней к текущей дате
    :param pattern: паттерн оформления даты. По умолчанию - DDMMYYYY

    """
    today = datetime.today()
    needed_date = today + timedelta(days=plus) if plus > 0 else today
    return needed_date.strftime(pattern)


def widget_weather(**kwargs):
    """
    Функция создает карточку с информацией о погоде.

    :param **kwargs: любое количество ключевых аргументов.

    :return dmc.Card: карточка с информацией о погоде.
    """
    return dmc.Card(
        [
            dmc.Text("Погода в г. Екатеринбург", size="xl", ta="center"),
            dmc.Space(h=5),
            dmc.Group(
                [
                    get_weather_label(get_date_string(0), ["+1", "-4"], "cloudy"),
                    get_weather_label(get_date_string(1), ["+10", "-4"], "sunny"),
                    get_weather_label(
                        get_date_string(2), ["+1", "-4"], "partly-cloudy"
                    ),
                    get_weather_label(
                        get_date_string(3), ["+10", "-4"], "thunderstorm"
                    ),
                    get_weather_label(get_date_string(4), ["+1", "-40"], "rain"),
                ],
                justify="center",
                gap="xs",
            ),
        ],
        className="mobile-block",
        shadow="md",
    )


def widget_torrents():
    """
    Функция создает карточку с информацией о торрентах.

    :return dmc.Card:
    """
    conn = db_connection.get_conn()
    settings = file_manager.get_settings(conn)

    qbt_ip = settings["apps.torrents.qbittorrent_ip"]
    qbt_port = settings["apps.torrents.qbittorrent_port"]

    return dmc.Card(
        [
            dmc.Text("Мониторинг торрентов", size="xl", ta="center"),
            dmc.Space(h=10),
            dmc.Stack(
                [
                    dmc.Text("Активных: NaN", id="home-torrents-active"),
                    dmc.Text("Скачивается: NaN", id="home-torrents-download"),
                    dmc.Text("Раздается: NaN", id="home-torrents-upload"),
                ],
                style={"text-align": "left"},
                gap="xs",
            ),
            dmc.Space(h=15),
            dmc.Anchor(
                "Открыть qbittorrent",
                href="http://" + qbt_ip + ":" + qbt_port,
                target="_blank",
            ),
            dmc.LoadingOverlay(
                visible=False,
                id="loading-overlay-widget-torrent",
                zIndex=200,
                overlayProps={"radius": "sm", "blur": 2},
            ),
        ],
        className="mobile-block",
        shadow="md",
        # style={"min-height": "100%"},
    )


def widget_systeminfo():
    """
    Функция создает карточку с информацией о системе.

    :return dmc.Card: карточка с информацией о системе.
    """

    cpu_usage = int(psutil.cpu_percent(interval=0.1))
    return dmc.Card(
        [
            dmc.Text("Системный монитор", size="xl", ta="center"),
            dmc.Space(h=10),
            dmc.Group(
                [
                    dmc.Stack(
                        [
                            dmc.Text("CPU", ta="center", fw=500),
                            dmc.RingProgress(
                                sections=[
                                    {
                                        "value": cpu_usage,
                                        "color": get_color_by_value(percent=cpu_usage),
                                        "tooltip": f"Используется: {cpu_usage}%",
                                    },
                                ],
                                label=dmc.Text(
                                    f"{round(psutil.cpu_freq().current / 1000, 2)} GHz",
                                    ta="center",
                                ),
                                size=120,
                                roundCaps=True,
                            ),
                        ],
                        gap=0,
                    ),
                    dmc.Stack(
                        [
                            dmc.Text("RAM", ta="center", fw=500),
                            dmc.RingProgress(
                                sections=[
                                    {
                                        "value": psutil.virtual_memory().percent,
                                        "color": get_color_by_value(
                                            percent=psutil.virtual_memory().percent
                                        ),
                                        "tooltip": f"Занято: {get_readable_bytes(psutil.virtual_memory().used)}",
                                    },
                                ],
                                label=dmc.Text(
                                    get_readable_bytes(psutil.virtual_memory().total),
                                    ta="center",
                                ),
                                size=120,
                                roundCaps=True,
                            ),
                        ],
                        gap=0,
                    ),
                    dmc.Stack(
                        [
                            dmc.Text("SWAP", ta="center", fw=500),
                            dmc.RingProgress(
                                sections=[
                                    {
                                        "value": psutil.swap_memory().percent,
                                        "color": get_color_by_value(
                                            percent=psutil.swap_memory().percent
                                        ),
                                        "tooltip": f"Занято: {get_readable_bytes(psutil.swap_memory().used)}",
                                    },
                                ],
                                label=dmc.Text(
                                    get_readable_bytes(psutil.swap_memory().total),
                                    ta="center",
                                ),
                                size=120,
                                roundCaps=True,
                            ),
                        ],
                        gap=0,
                    ),
                ],
                justify="center",
            ),
            dmc.Divider(h=10),
            dmc.Group(
                [
                    dmc.Group(
                        [
                            dmc.Text("↓", fw=600),
                            dmc.Text("NaN b/s"),
                        ],
                        justify="center",
                        c="#369e1f",
                        w="max-content",
                    ),
                    dmc.Group(
                        [
                            dmc.Text("↑", fw=600),
                            dmc.Text("NaN b/s"),
                        ],
                        justify="center",
                        c="custom-primary-color",
                        w="max-content",
                    ),
                ],
                # w="100%",
                grow=True,
                style={"flex-wrap": "nowrap"},
            ),
        ],
        className="mobile-block",
        shadow="md",
        w='100%'
    )


def widget_file_manager_log():
    """

    :return: None
    """
    # статистика по добавленным файлам
    return None
