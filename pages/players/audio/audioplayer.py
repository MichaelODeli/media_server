import dash_mantine_components as dmc
import dash_player
from dash import (ALL, Input, Output, State, callback, ctx,
                  html, register_page)
from dash.exceptions import PreventUpdate
from flask import request

from controllers import cont_audioplayer as cont_a
from controllers import cont_media as cont_m
from controllers import db_connection
from controllers import service_controller as service
from views import v_audioplayer

register_page(__name__, path="/players/audio", icon="fa-solid:home")


def layout(l="n", playlist_id=0, artist_id=0, album_id=0, **kwargs):  # noqa: E741
    """

    :param l:
    :param playlist_id:
    :param artist_id:
    :param album_id:
    :param kwargs:
    :return:
    """
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        service.log_printer(request.remote_addr, "audioplayer", "page opened")

        conn = db_connection.get_conn()

        if playlist_id == 0 and artist_id == 0 and album_id == 0:
            page_name = "Главная"
            page_content = v_audioplayer.render_main_page()
        else:
            if playlist_id != 0 and artist_id == 0 and album_id == 0:
                page_name = "Какой-то плейлист"
                page_content = v_audioplayer.render_playlist_page(conn, playlist_id)
            elif artist_id != 0 and playlist_id == 0 and album_id == 0:
                page_name = "Какой-то исполнитель"
                page_content = v_audioplayer.render_artist_page(artist_id)
            elif album_id != 0 and playlist_id == 0 and artist_id == 0:
                page_name = "Какой-то альбом"
                page_content = v_audioplayer.render_album_page(album_id)
            else:
                page_name = ""
                page_content = html.Center(dmc.Title("Ошибка идентификатора.", order=4))

        return dmc.AppShell(
            children=[
                dmc.AppShellNavbar(
                    v_audioplayer.render_audio_navbar(source="col", conn=conn),
                    className="border-end-0",
                ),
                dmc.AppShellMain(
                    [
                        dash_player.DashPlayer(
                            id="audio-player",
                            url="https://www.youtube.com/watch?v=4xnsmyI5KMQ&t=1s",
                            width="0",
                            height="0",
                            style={"display": "none"},
                            intervalCurrentTime=500,
                            volume=20,
                        ),
                        dmc.Space(),
                        dmc.Stack(
                            [
                                dmc.Title(
                                    page_name,
                                    order=3,
                                    id="audioplayer-playlist-name",
                                ),
                                dmc.Space(),
                                dmc.Group(id="audio-playlist-description"),
                                dmc.ScrollArea(
                                    children=page_content,
                                    id="audioplayer-children",
                                    pb="sm",
                                    h="70dvh",
                                    offsetScrollbars=True,
                                ),
                            ],
                            gap="xs",
                        ),
                        v_audioplayer.render_audio_navbar_drawer(conn),
                    ],
                    className="border-start overflow-hidden no-border-mobile",
                    mah="calc(100dvh - var(--app-shell-header-height) - 10px) !important",
                    mih="calc(100dvh - var(--app-shell-header-height) - 10px) !important",
                    ps='sm',
                    pt='.25rem'
                ),
                dmc.AppShellFooter(v_audioplayer.render_audio_footer()),
            ],
            navbar={
                "width": 300,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
            footer={"height": "auto"},
            pt=20,
            maw={"base": "unset", "md": "100%"},
            id="dummy-3",
            # mah="90dvh",
        )


@callback(
    Output("drawer-albums", "opened", allow_duplicate=True),
    Input("open-drawer-albums", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_with_albums(n_clicks):
    """

    :param n_clicks:
    :return:
    """
    return True


@callback(
    [Output("audio-player", "playing"), Output("playpause-icon", "icon")],
    Input("control-playpause", "n_clicks"),
    State("audio-player", "playing"),
    prevent_initial_call=True,
)
def player_play_pause(n_clicks, playing):
    """

    :param n_clicks:
    :param playing:
    :return:
    """
    if not playing:
        icon = "material-symbols:pause"
    else:
        icon = "material-symbols:play-arrow"
    return not playing, icon


@callback(
    [Output("audio-player", "loop"), Output("loop-icon", "icon")],
    Input("control-repeat", "n_clicks"),
    State("audio-player", "loop"),
    prevent_initial_call=True,
)
def player_loop(n_clicks, loop):
    """

    :param n_clicks:
    :param loop:
    :return:
    """
    if not loop:
        icon = "material-symbols:repeat-on"
    else:
        icon = "material-symbols:repeat"
    return not loop, icon


@callback(
    [Output("audio-player", "muted"), Output("muted-icon", "icon")],
    Input("volume-muted", "n_clicks"),
    State("audio-player", "muted"),
    prevent_initial_call=True,
)
def player_disable_sound(n_clicks, muted):
    """

    :param n_clicks:
    :param muted:
    :return:
    """
    if not muted:
        icon = "material-symbols:volume-off"
    else:
        icon = "material-symbols:volume-up"
    return not muted, icon


@callback(
    Output("audio-player", "volume"),
    Input("volume-slider", "value"),
    State("audio-player", "volume"),
    # prevent_initial_call=True,
)
def player_volume_slider(volume_value, current_vol):
    """

    :param volume_value:
    :param current_vol:
    :return:
    """
    return volume_value / 100


@callback(
    [
        Output("progress-slider", "value"),
        Output("progress-slider", "max"),
        Output("audio-current-time", "children"),
        Output("audio-full-time", "children"),
    ],
    Input("audio-player", "currentTime"),
    State("audio-player", "duration"),
    prevent_initial_call=True,
)
def player_volume(current_time, duration):
    """

    :param current_time:
    :param duration:
    :return:
    """
    current_time = int(current_time) if current_time is not None else 0
    duration = int(duration) if duration is not None else 0

    return (
        current_time,
        duration,
        cont_m.get_duration(current_time),
        cont_m.get_duration(duration),
    )


@callback(
    Output({"type": "audio-playlist-btn-col", "id": ALL}, "n_clicks"),
    Output({"type": "audio-playlist-btn-drawer", "id": ALL}, "n_clicks"),
    Output("audioplayer-playlist-name", "children"),
    Output("drawer-albums", "opened"),
    Output("audio-playlist-description", "children"),
    Output("audioplayer-children", "children"),
    Input({"type": "audio-playlist-btn-col", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-drawer", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-home", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-search", "id": ALL}, "n_clicks"),
    State({"type": "audio-playlist-btn-col", "id": ALL}, "id"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def select_page_from_leftside_row(
    n_clicks_col, n_clicks_drawer, n_clicks_home, n_clicks_search, button_ids, pathname
):
    """

    :param n_clicks_col:
    :param n_clicks_drawer:
    :param n_clicks_home:
    :param n_clicks_search:
    :param button_ids:
    :param pathname:
    :return:
    """
    types_ids = [i["id"] for i in button_ids]

    if (
        n_clicks_col == [None] * len(n_clicks_col)
        and n_clicks_drawer == [None] * len(n_clicks_drawer)
        and n_clicks_home == [None] * len(n_clicks_home)
        and n_clicks_search == [None] * len(n_clicks_search)
    ):
        raise PreventUpdate

    description = None
    if ctx.triggered_id["type"] == "audio-playlist-btn-home":
        page_name = "Главная"
        player_children = [v_audioplayer.render_main_page()]
    elif ctx.triggered_id["type"] == "audio-playlist-btn-search":
        page_name = "Поиск"
        player_children = [v_audioplayer.render_search_page()]
    else:

        if ctx.triggered_id["type"] == "audio-playlist-btn-col":
            selected_type = types_ids[n_clicks_col.index(1)]
        elif ctx.triggered_id["type"] == "audio-playlist-btn-drawer":
            selected_type = types_ids[n_clicks_drawer.index(1)]
        else:
            raise PreventUpdate

        conn = db_connection.get_conn()
        page_name = cont_a.get_audio_types(conn, type_id=selected_type)[0]["type_name"]

        player_children = v_audioplayer.render_playlist_page(conn, selected_type)

        description = [
            dmc.Badge("Много треков", variant="light"),
        ]

    return (
        [None] * len(n_clicks_col),
        [None] * len(n_clicks_drawer),
        page_name,
        False,
        description,
        player_children,
    )
