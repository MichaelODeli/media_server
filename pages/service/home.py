import dash_mantine_components as dmc
from dash import (Input, Output, callback, register_page)
from flask import request

from controllers import cont_homepage
from controllers import service_controller as service

register_page(__name__, path="/", icon="fa-solid:home")


def layout():
    """

    :return:
    """
    lay = dmc.Container(
        children=[
            dmc.Grid(
                [
                    dmc.GridCol(
                        [cont_homepage.widget_systeminfo()],
                        span="content",
                        w={"base": "100%", "sm": "unset"} 
                    ),
                    dmc.GridCol(
                        [cont_homepage.widget_disk_size()],
                        span="content",
                        id="t",
                        w={"base": "100%", "sm": "unset"} 
                    ),
                    dmc.GridCol(
                        [cont_homepage.widget_torrents()],
                        span="content",
                        id="widgetTorrents",
                        w={"base": "100%", "sm": "unset"} 
                    ),
                    dmc.GridCol(
                        [cont_homepage.widget_weather()],
                        span="content",
                        id="widget-weather",
                        w={"base": "100%", "sm": "unset"} 
                    ),
                ],
                align="stretch",
                justify="center",
                display={"base": "flex", "sm": "block"} 
            ),
        ],
        pt=20,
        # style={"paddingTop": 20},
        className="dmc-container",
        maw={"base": "unset", "md": "100%"}
    )

    # print(f'{request.remote_addr} - - [{now}] | homepage {request.base_url}')
    service.log_printer(request.remote_addr, "homepage", "page opened")
    return lay


@callback(
    [
        Output("home-torrents-active", "children"),
        Output("home-torrents-download", "children"),
        Output("home-torrents-upload", "children"),
    ],
    [Input("t", "children")],
    running=[(Output("loading-overlay-widget-torrent", "visible"), True, False)]
)
def render_torrents_status(_):
    """

    :param _:
    :return:
    """
    return cont_homepage.get_torrent_status()
