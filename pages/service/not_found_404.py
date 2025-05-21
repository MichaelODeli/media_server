import dash_mantine_components as dmc
from dash import register_page

register_page(__name__)


def layout(**kwargs):
    """

    :param kwargs:
    :return:
    """
    return dmc.Container(
        children=[
            dmc.Stack(
                [dmc.Title("Страница не найдена.", order=3), dmc.Anchor('На главную', href='/')],
                justify="center",
                align="center",
            )
        ],
        w="100%",
        pt='md'
    )
