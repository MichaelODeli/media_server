from datetime import datetime, timedelta

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


# import datetime


def log_printer(client, page, data):
    """
    Вывод строки с датой и необходимой информацией
    """
    with open("logs/main.log", "a", encoding="UTF-8") as file:
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S.%f")[:-3]
        string = f"{client} - - [{now}] | {page} | {data}"
        print(string, file=file)  # output to file
        print(string)


def numeral_noun_declension(
    number, nominative_singular, genetive_singular, nominative_plural
):
    """

    :param number:
    :param nominative_singular:
    :param genetive_singular:
    :param nominative_plural:
    :return:
    """
    return (
        (number in range(5, 20))
        and nominative_plural  # noqa: W503
        or (1 in (number, (diglast := number % 10)))  # noqa: W503
        and nominative_singular  # noqa: W503
        or ({number, diglast} & {2, 3, 4})  # noqa: W503
        and genetive_singular  # noqa: W503
        or nominative_plural  # noqa: W503
    )


def get_date_difference(date):
    """

    :param date:
    :return:
    """
    # Получаем текущую дату
    today = date.today()

    # Вычисляем количество дней между сегодняшней датой и заданной
    days_diff = (today - date).days
    if days_diff < 0:
        raise ValueError("Заданная дата больше текущей")

    if days_diff == 0:
        return "сегодня"
    elif days_diff == 1:
        return "вчера"
    elif days_diff <= 7:
        return (
            str(days_diff)
            + " "
            + numeral_noun_declension(days_diff, "день", "дня", "дней")
            + " назад"
        )
    elif 7 < days_diff <= 30:
        weeks_diff = days_diff // 7
        return (
            str(weeks_diff)
            + " "
            + numeral_noun_declension(weeks_diff, "неделя", "недели", "недель")
            + " назад"
        )
    else:
        years_diff = int((today - date) / timedelta(days=365))
        months_diff = int(round((today - date) / timedelta(days=30)))
        if years_diff > 0:
            return (
                str(years_diff)
                + " "
                + numeral_noun_declension(years_diff, "год", "года", "лет")
                + " назад"
            )
        elif months_diff > 0:
            return (
                str(months_diff)
                + " "
                + numeral_noun_declension(months_diff,
                                          "месяц", "месяца", "месяцев")
                + " назад"
            )
        else:
            return "более месяца назад"


# function for generating Dash Iconify content
def get_icon(
    icon, size=18, background=True, icon_color="white", background_color="black"
):
    """
    Функция getIcon возвращает иконку с заданными параметрами.

    :param background_color:
    :param icon: имя иконки
    :param size: размер иконки
    :param background: флаг, указывающий на необходимость отображения фона у иконки
    :param icon_color: цвет иконки
    :return: иконка с заданными параметрами
    """

    if icon_color == "primary":
        icon_color = "custom-primary-color"
    return (
        dmc.ThemeIcon(
            DashIconify(icon=icon, width=size, color=icon_color),
            size=size,
            radius=size + 7,
            # variant="subtle",
            color=background_color,
            m="5px",
        )
        if background
        else DashIconify(icon=icon, width=size, color=icon_color)
    )


def get_button_with_icon(
    button_icon, button_title, button_id, disabled=False, color=None
):
    """

    :param button_icon:
    :param button_title:
    :param button_id:
    :param disabled:
    :param color:
    :return:
    """
    return dmc.Button(
        DashIconify(
            icon=button_icon,
            width=25,
        ),
        variant='outline',
        color=color,
        id=button_id,
        className="button-center-content",
        disabled=disabled,
        n_clicks=0,
    )

    # return dmc.Tooltip(
    #     label=button_title,
    #     position="top",
    #     offset=3,
    #     withArrow=True,
    #     children=[
    #         dmc.Button(
    #             DashIconify(
    #                 icon=button_icon,
    #                 width=25,
    #             ),
    #             variant="outline",
    #             color=color,
    #             id=button_id,
    #             className="button-center-content",
    #             disabled=disabled,
    #             n_clicks=0,
    #         )
    #     ],
    # )


def dmc_color(color_name: str, color_id: int):
    """

    :param color_name:
    :param color_id:
    :return:
    """
    return dmc.DEFAULT_THEME["colors"][color_name][color_id]


def dmc_button_link(
    button_label, href, target=None, button_left_icon=None, button_right_icon=None, height='max-content', class_name=''
):
    """

    :param button_label:
    :param href:
    :param target:
    :param button_left_icon:
    :param button_right_icon:
    :param height:
    :param class_name:
    :return:
    """
    return html.A(
        children=dmc.Group(
            [
                DashIconify(
                    icon=button_left_icon) if button_left_icon is not None else None,
                dmc.Text(
                    button_label,
                    className="m_811560b9 mantine-Button-label",
                    size="sm",
                    style={"height": "max-content"},
                ),
                DashIconify(
                    icon=button_right_icon) if button_right_icon is not None else None,
            ],
            gap="xs",
            wrap="nowrap",
            className="m_80f1301b mantine-Button-inner",
            style={"height": "max-content"},
            py=5,
        ),
        href=href,
        target=target,
        className="mantine-focus-auto mantine-active m_77c9d27d mantine-Button-root m_87cf2631 mantine-UnstyledButton-root center-content mantine-sm-button" +
                  " " + class_name,
        style={"width": "max-content", "height": height},
    )


def dmc_button_from_html(
    button_label, button_left_icon=None, button_right_icon=None, height='max-content'
):
    """

    :param button_label:
    :param button_left_icon:
    :param button_right_icon:
    :param height:
    :return:
    """
    return html.Button(
        children=dmc.Group(
            [
                DashIconify(
                    icon=button_left_icon) if button_left_icon is not None else None,
                dmc.Text(
                    button_label,
                    className="m_811560b9 mantine-Button-label",
                    size="sm",
                    style={"height": "max-content"},
                ),
                DashIconify(
                    icon=button_right_icon) if button_right_icon is not None else None,
            ],
            gap="xs",
            wrap="nowrap",
            className="m_80f1301b mantine-Button-inner",
            style={"height": "max-content"},
            py=5,
        ),
        className="mantine-focus-auto mantine-active m_77c9d27d mantine-Button-root m_87cf2631 mantine-UnstyledButton-root center-content mantine-sm-button",
        style={"width": "max-content", "height": height},
    )
