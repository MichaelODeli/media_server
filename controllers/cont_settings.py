import platform

import dash_mantine_components as dmc
import psutil
from dash import dcc, html


def generate_table_row(param_name: str, param_value="", head=False):
    """Генерация строки в таблице

    :param param_name: Данные для 1 столбца
    :param param_value: Данные для 2 столбца
    :param (bool) head: Заголовок
    :return:
    """
    return dmc.TableTr(
        [
            (
                dmc.TableTd(
                    param_name,
                    className="min-column-width center-content-vertical",
                    style={"padding": "0.3rem" if param_value != "" else "1rem"},
                )
                if not head
                else dmc.TableTh(param_name, className="min-column-width")
            ),
            (
                dmc.TableTd(
                    param_value,
                    style={"padding": "0.3rem" if param_value != "" else "1rem"},
                )
                if not head
                else dmc.TableTh(param_value)
            ),
        ]
    )


def get_readable_bytes(bytes_value, suffix="B") -> str:
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'

    :param bytes_value: число для конвертации
    :return (str):
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_value < factor:
            return f"{bytes_value:.2f}{unit}{suffix}"
        bytes_value /= factor


def get_system_info_rows() -> list:
    """Получение строк с информацией о системе

    :return (list):
    """
    uname = platform.uname()
    return [
        generate_table_row(dmc.Title("Информация о системе", order=5)),
        generate_table_row("Операционная система", f"{uname.system}"),
        generate_table_row("Идентификатор устройства", f"{uname.node}"),
        generate_table_row("Релиз", f"{uname.release}"),
        generate_table_row("Версия ОС", f"{uname.version}"),
        generate_table_row("Архитектура", f"{uname.machine}"),
        generate_table_row("Процессор", f"{uname.processor}"),
    ]


def get_cpu_info_rows():
    """Получить информацию о ЦП

    :return (list):
    """
    cpufreq = psutil.cpu_freq()
    return [
        generate_table_row(dmc.Title("Информация о процессоре", order=5)),
        generate_table_row(
            "Физических/логических ядер",
            f"{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}",
        ),
        generate_table_row(
            "Базовая частота",
            f"{cpufreq.current:.2f}Mhz",
        ),
        generate_table_row(
            "Использование ядер процессора",
            html.Div(
                [
                    dmc.Button(
                        "Показать",
                        id="show-cpu-load",
                    )
                ],
                id="cpu-ring-usage",
            ),
        ),
        generate_table_row(
            "Использование процессора",
            f"{psutil.cpu_percent(interval=0.1)}%",
        ),
    ]


def get_ram_swap_info_rows():
    """Получить информацию о ОЗУ и SWAP

    :return (list):
    """
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return [
        generate_table_row(dmc.Title("ОЗУ", order=5)),
        generate_table_row("Всего", f"{get_readable_bytes(svmem.total)}"),
        generate_table_row(
            "Доступно",
            f"{get_readable_bytes(svmem.available)}",
        ),
        generate_table_row("Использовано", f"{get_readable_bytes(svmem.used)}"),
        generate_table_row("Процент использования", f"{svmem.percent}%"),
        generate_table_row(dmc.Title("SWAP", order=5)),
        generate_table_row("Всего", f"{get_readable_bytes(swap.total)}"),
        generate_table_row("Свободно", f"{get_readable_bytes(swap.free)}"),
        generate_table_row("Использовано", f"{get_readable_bytes(swap.used)}"),
        generate_table_row("Процент использования", f"{swap.percent}%"),
    ]


def get_partitions_info_rows():
    """Получить информацию о разделах дисков

    :return (list):
    """
    partitions = psutil.disk_partitions()
    parts_data = []
    for partition in partitions:
        partition_data = [
            dcc.Markdown(
                f"**Устройство**: {partition.device}", className="partition-no-margin"
            ),
            dcc.Markdown(
                f"**Точка монтирования**: {partition.mountpoint}",
                className="partition-no-margin",
            ),
            dcc.Markdown(
                f"**Файловая система**: {partition.fstype}",
                className="partition-no-margin",
            ),
        ]
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            partition_data.append(
                dcc.Markdown(
                    f"**Всего доступно**: {get_readable_bytes(partition_usage.total)}",
                    className="partition-no-margin",
                )
            )
            partition_data.append(
                dcc.Markdown(
                    f"**Использовано**: {get_readable_bytes(partition_usage.used)}",
                    className="partition-no-margin",
                )
            )
            partition_data.append(
                dcc.Markdown(
                    f"**Свободно**: {get_readable_bytes(partition_usage.free)}",
                    className="partition-no-margin",
                )
            )
            partition_data.append(
                dcc.Markdown(
                    f"**Процент использования**: {partition_usage.percent}%",
                    className="partition-no-margin",
                )
            )
        except PermissionError:
            continue
        parts_data.append(
            generate_table_row(partition.device, dmc.Stack(partition_data, gap=0))
        )

    return [generate_table_row(dmc.Title("Накопители и разделы", order=5))] + parts_data
