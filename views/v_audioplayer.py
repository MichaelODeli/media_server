import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from controllers.cont_audioplayer import get_audio_dict, get_audio_types
from controllers.cont_media import get_duration


def render_main_page(conn=None):
    """

    :param conn: db connection to PostgreSQL
    :return:
    """
    return dmc.Stack(
        [
            html.A(
                "Страница исполнителя",
                href="/players/audio?l=y&artist_id=90",
                className="a-color",
            ),
            html.A(
                "Страница плейлиста",
                href="/players/audio?l=y&playlist_id=90",
                className="a-color",
            ),
            html.A(
                "Страница альбома",
                href="/players/audio?l=y&album_id=90",
                className="a-color",
            ),
        ]
    )


def render_search_page(conn=None):
    """

    :param conn: db connection to PostgreSQL
    :return:
    """
    return "Поиск"


def render_playlist_page(conn, playlist_id):
    """

    :param conn: db connection to PostgreSQL
    :param playlist_id:
    :return:
    """
    return dmc.Table(
        # hover=True,
        children=[
            dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh(className="min-column-width", px="sm"),
                        dmc.TableTh(className="min-column-width", px="sm"),
                        dmc.TableTh("Название", px="sm"),
                        dmc.TableTh(
                            "Альбом",
                            px="sm",
                            display={"base": "none", "md": "table-cell"},
                        ),
                        dmc.TableTh(
                            "Загружено",
                            className="min-column-width center-content",
                            px="sm",
                            display={"base": "none", "md": "table-cell"},
                        ),
                        dmc.TableTh(
                            "🕑", className="min-column-width center-content", px="sm"
                        ),
                    ]
                ),
                className="sticky-th",
            ),
            dmc.TableTbody(
                className="audio-content",
                children=[
                    dmc.TableTr(
                        [
                            dmc.TableTd(
                                dmc.ActionIcon(
                                    radius="xl",
                                    children=DashIconify(icon="mdi:play"),
                                ),
                                className="min-column-width",
                                p="xs",
                            ),
                            dmc.TableTd(
                                dmc.Avatar(radius="sm"),
                                className="min-column-width",
                                p="xs",
                            ),
                            dmc.TableTd(
                                dmc.Stack(
                                    [
                                        dmc.Text(
                                            audio_data["audio_title"]
                                            if audio_data["audio_title"] is not None
                                            else ".".join(
                                                audio_data["file_name"].split(".")[:-1]
                                            )
                                        ),
                                        html.A(
                                            (
                                                audio_data["artist"]
                                                if audio_data["artist"] is not None
                                                else "Неизвестен"
                                            ),
                                            className="audio-link w-content",
                                            href=f"/file_id={audio_data['file_id']}",
                                        ),
                                    ],
                                    gap=0,
                                ),
                                p="sm",
                            ),
                            dmc.TableTd(
                                html.A(
                                    (
                                        audio_data["album_title"]
                                        if audio_data["album_title"] is not None
                                        else ""
                                    ),
                                    className="audio-link w-content",
                                    href="#",
                                ),
                                display={"base": "none", "md": "table-cell"},
                                p="xs",
                            ),
                            dmc.TableTd(
                                "Недавно",
                                className="min-column-width",
                                display={"base": "none", "md": "table-cell"},
                                p='xs'
                            ),
                            dmc.TableTd(
                                (
                                    get_duration(audio_data["audio_duration"])
                                    if (audio_data["audio_duration"] is not None)
                                    else "00:00"
                                ),
                                className="min-column-width",
                                p='xs'
                            ),
                        ]
                    )
                    for audio_data in get_audio_dict(conn, playlist_id)
                ],
            ),
        ],
        className="no-box-shadow",
        highlightOnHover=True,
        w='100%'
    )


def render_artist_page(artist_id=0):
    """

    :param artist_id:
    :return:
    """
    return "Какой-то артист"


def render_album_page(album_id=0):
    """

    :param album_id:
    :return:
    """
    return "Какой-то альбом"


def render_audio_navbar(source, conn):
    """

    :param source:
    :param conn: db connection to PostgreSQL
    :return:
    """
    if source != "col" and source != "drawer":
        raise ValueError

    content = dmc.Stack(
        [
            dmc.NavLink(
                leftSection=DashIconify(
                    icon="material-symbols:home",
                    width=25,
                    style={"margin-right": "5px"},
                ),
                label="Главная",
                id={
                    "type": "audio-playlist-btn-home",
                    "id": 1 if source == "col" else 2,
                },
            ),
            dmc.NavLink(
                leftSection=DashIconify(
                    icon="material-symbols:search",
                    width=25,
                    style={"margin-right": "5px"},
                ),
                label="Поиск музыки",
                id={
                    "type": "audio-playlist-btn-search",
                    "id": 1 if source == "col" else 2,
                },
            ),
            dmc.NavLink(
                leftSection=DashIconify(
                    icon="mdi:music",
                    width=25,
                    style={"margin-right": "5px"},
                ),
                label="Медиатека",
                opened=True,
                children=[
                    dmc.NavLink(
                        leftSection=DashIconify(
                            icon="material-symbols:playlist-play",
                            width=25,
                            style={"margin-right": "5px"},
                        ),
                        label=audio_type["type_name"],
                        id={
                            "type": f"audio-playlist-btn-{source}",
                            "id": audio_type["type_id"],
                        },
                    )
                    for audio_type in get_audio_types(conn)
                ],
            ),
        ],
        gap=0,
        ms="sm",
    )

    return content


def render_audio_navbar_drawer(conn):
    """

    :param conn: db connection to PostgreSQL
    :return:
    """
    return dmc.Drawer(
        children=[render_audio_navbar(source="drawer", conn=conn)],
        title=dmc.Title("Аудиоплеер", order=4),
        id="drawer-albums",
        padding="md",
        zIndex=10000,
        style={"overflow-y": "auto"},
    )


def render_audio_footer():
    """

    :return:
    """
    return dmc.Grid(
        [
            dmc.GridCol(
                [
                    dmc.ActionIcon(
                        DashIconify(
                            icon="iconamoon:menu-burger-horizontal",
                            width=35,
                        ),
                        size="40px",
                        radius="md",
                        variant="default",
                        id="open-drawer-albums",
                        className="shown-affix",
                    ),
                ],
                span="content",
            ),
            dmc.GridCol(
                dmc.Stack(
                    [
                        dmc.Text(
                            "Название песни",
                            className="text-default",
                            # style={"margin-bottom": 0, "font-weight": "bold"},
                            id="song-name",
                            fw=600,
                        ),
                        dmc.Text(
                            "Исполнитель",
                            className="text-default",
                            style={"margin-bottom": 0},
                            id="song-artist",
                        ),
                    ],
                    gap=0,
                ),
                span="content",
            ),
            dmc.GridCol(
                [
                    dmc.Stack(
                        [
                            dmc.Group(
                                [
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:shuffle",
                                            width=25,
                                            color="dark",
                                        ),
                                        id="control-shuffle",
                                        display={"base": "none", "md": "block"},
                                        variant="subtle",
                                        size="lg",
                                        color="default",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:skip-previous",
                                            width=25,
                                            color="dark",
                                        ),
                                        id="control-prev",
                                        variant="subtle",
                                        size="lg",
                                        color="default",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:play-pause",
                                            width=30,
                                            id="playpause-icon",
                                        ),
                                        id="control-playpause",
                                        variant="filled",
                                        size="xl",
                                        radius="xl",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:skip-next",
                                            width=25,
                                            color="dark",
                                        ),
                                        id="control-next",
                                        variant="subtle",
                                        size="lg",
                                        color="default",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:repeat",
                                            width=25,
                                            color="dark",
                                            id="loop-icon",
                                        ),
                                        id="control-repeat",
                                        variant="subtle",
                                        size="lg",
                                        color="default",
                                    ),
                                ],
                                align="center",
                                style={"justify-content": "center"},
                                gap="xs",
                            ),
                            dmc.Group(
                                [
                                    dmc.Text("00:00", id="audio-current-time"),
                                    dmc.Slider(
                                        min=0,
                                        max=100,
                                        id="progress-slider",
                                        value=0,
                                        w="70%",
                                        color="gray.7",
                                        showLabelOnHover=False,
                                        # disabled=True
                                    ),
                                    dmc.Text(
                                        "00:00",
                                        id="audio-full-time",
                                        className="hided_element",
                                    ),
                                ],
                                gap="sm",
                                align="center",
                                style={"justify-content": "center"},
                            ),
                        ],
                        gap=0,
                    ),
                ],
                span="auto",
                p=0,
            ),
            dmc.GridCol(
                [
                    dmc.ActionIcon(
                        DashIconify(
                            icon="material-symbols:volume-up",
                            width=30,
                            color="dark",
                            id="muted-icon",
                        ),
                        id="volume-muted",
                        variant="subtle",
                        size="xl",
                        color="default",
                    ),
                    dmc.Slider(
                        min=0,
                        max=100,
                        id="volume-slider",
                        value=20,
                        w="120px",
                        color="gray.7",
                        thumbLabel="Громкость",
                        updatemode="drag",
                    ),
                ],
                span="content",
                style={"align-items": "center", "display": "flex"},
                className="hided_element",
            ),
        ],
        align="center",
        justify="center",
        className="block-background-float",
        py="md",
    )
