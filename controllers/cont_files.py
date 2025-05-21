from random import randint as r

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_extensions import Purify
from dash_iconify import DashIconify


def nested_list_to_html(lst):
    """
    Рекурсивно преобразует вложенный список в маркированный список HTML.

    :param lst (list): Вложенный список, который нужно преобразовать.
    :return (str): Строка, содержащая HTML-код маркированного списка.

    Для выделения текста жирным шрифтом, оберните текст в звездочки: *text*.
    """
    html = "<ul>\n"
    for item in lst:
        if isinstance(item, list):
            html += nested_list_to_html(item)
        else:
            if str(item)[0] == "*" and str(item)[-1] == "*":
                html += "<li><b>" + str(item)[1:-1] + "</b></li>\n"
            else:
                html += "<li>" + str(item) + "</li>\n"
    html += "</ul>\n"
    return html.replace("\n", "")


def generate_html_table(
    header: list,
    data: list,
    align="right",
    variant="full",
    striped=False,
    highlight_on_hover=False,
):
    """
    Генерирует HTML-таблицу на основе переданных заголовков и данных.

    :param header (list): Список заголовков столбцов таблицы.
    :param data (list): Список списков, представляющих строки данных таблицы.
    :param align (str): Выравнивание элементов таблицы
    :param variant (str): full/compact

    :return html.Div: HTML-элемент div, содержащий таблицу.
    """
    header = [
        dmc.TableThead(
            dmc.TableTr(
                [dmc.TableTh(header[0], style={"max-width": "20px"})] +
                [
                    dmc.TableTh(
                        header_element,
                        style={
                            "text-align": 'center'
                        },
                    )
                    for header_element in header[1:]
                ]
            )
        )
    ]
    body = [
        dmc.TableTbody(
            [
                dmc.TableTr(
                    [
                        dmc.TableTd(
                            value,
                            style={
                                "align-content": 'center',
                                "padding": (
                                    "5px" if variant == "compact" else "unset"
                                ),
                            },
                        )
                        for value in row_data
                    ]
                )
                for row_data in data
            ]
        )
    ]

    return html.Div(
        [
            dmc.Table(
                header + body,
                striped=striped,
                highlightOnHover=highlight_on_hover,
                style={"box-shadow": "unset", "text-align": align},
            )
        ],
        style={
            "overflow-x": "auto",
            "white-space": "nowrap",
            # "padding": "0" if variant == "compact" else "unset",
        },
    )


def block_files_list():
    """

    :return html.Div:
    """
    return html.Div(
        [
            dmc.Grid(
                [
                    dmc.GridCol(
                        dmc.Title("Менеджер файлов", style={"margin": "0"}, order=5),
                        span="content",
                    ),
                    dmc.GridCol(span="auto"),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                DashIconify(
                                    icon="material-symbols:file-copy", width=20
                                ),
                                outline=True,
                                color="primary",
                                id="files-copy-button",
                                className="button-center-content",
                                title="Скопировать выбранные файлы",
                                disabled=True,
                                size="sm",
                            ),
                            dbc.Button(
                                DashIconify(
                                    icon="material-symbols:drive-file-move", width=20
                                ),
                                outline=True,
                                color="primary",
                                id="files-move-button",
                                className="button-center-content",
                                title="Переместить выбранные файлы",
                                disabled=True,
                                size="sm",
                            ),
                            dbc.Button(
                                DashIconify(icon="material-symbols:delete", width=20),
                                outline=True,
                                color="danger",
                                id="files-delete-button",
                                className="button-center-content",
                                title="Удалить выбранные файлы",
                                disabled=True,
                                size="sm",
                            ),
                        ],
                        style={"margin": "5px"},
                    ),
                ],
                align="stretch",
                justify="center",
            ),
            dmc.Space(h=15),
            generate_html_table(
                ["Маркер", "Название файла", "Размер", "Дата добавления", "Действия"],
                [
                    [
                        DashIconify(icon="material-symbols:folder", width=20),
                        "Перейти в каталог выше",
                        None,
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                ],
                align="center",
            ),
        ],
        className="block-background",
    )


def tree_content(source):
    """

    :param source: col/drawer
    :return (dmc.Stack):
    """
    if source == "col":
        label = "Hello! This is on column!"
    elif source == "drawer":
        label = "Hello! This is on drawer!"
    else:
        raise ValueError

    return dmc.Stack(
        [
            label,
            Purify(
                html=nested_list_to_html(
                    [
                        "C:/",
                        [
                            "Windows",
                            ["System32", "*SysWOW64*"],
                            "Program Files",
                            "Program Files (x86)",
                        ],
                    ]
                )
            )
        ]
    )


def get_drawer():
    """

    :return:
    """
    return dmc.Drawer(
        children=[tree_content(source="drawer")],
        title=dmc.Title("Дерево папок", order=5),
        id="drawer-tree",
        padding="md",
        zIndex=10000,
    )
