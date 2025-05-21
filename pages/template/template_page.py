import dash_mantine_components as dmc
from dash import (register_page)
from flask import request

from controllers import service_controller as service

register_page(__name__, path="/template", icon="fa-solid:home")


def layout(l='n', **kwargs):  # noqa: E741
    """

    :param l:
    :param kwargs:
    :return:
    """
    # lazy load block
    if l == 'n':
        return dmc.Container()
    else:
        service.log_printer(request.remote_addr, 'temp_page', 'page opened')
        # all workers must be here!
        return dmc.Container(
            children=[],
            pt=20,
            # style={"paddingTop": 20},
            className='dmc-container',
        )
