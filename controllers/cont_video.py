import dash_mantine_components as dmc
from dash import html

from controllers import cont_media


def get_search_link(category_id, type_id):
    """

    :param category_id:
    :param type_id:
    :return:
    """
    return f"/players/video/search?l=y&auto_search=y&category_id={category_id}&type_id={type_id}&from_video=y"


def create_video_miniature_container(
    href,
    video_title,
    videotype_name,
    date="недавно",
    img_video="/assets/img/image-not-found.jpg",
    # img_video="https://placehold.co/250x140",
    img_channel=None,
    video_duration=0,
    category_id=None,
    type_id=None,
):
    """
    Функция createVideoMiniaturesContainer создает контейнер для видео миниатюр.

    :param href:
    :param video_title:
    :param videotype_name:
    :param date:
    :param img_video:
    :param img_channel:
    :param video_duration:
    :param category_id:
    :param type_id:
    :return html.A: миниатюры видео.
    """
    return html.A(
        className="td-none",
        href=href,
        children=[
            dmc.Container(
                p=0,
                mt="xs",
                mb="sm",
                mx='xs',
                maw="250px",
                children=[
                    dmc.AspectRatio(
                        html.Div(
                            dmc.Text(
                                cont_media.get_duration(video_duration),
                                c="white",
                                bg="black",
                                w="max-content",
                                h="max-content",
                                className="video-time",
                                size="sm",
                                m='.25rem',
                                px='.25rem'
                            )
                        ),
                        ratio=16 / 9,
                        mb="xs",
                        w=250,
                        className="video-background-image",
                        style={"background-image": f"url('{img_video}')"},
                        pos='relative'
                    ),
                    dmc.Flex(
                        direction="row",
                        children=[
                            dmc.Avatar(radius="xl", src=img_channel),
                            dmc.Container(
                                children=[
                                    dmc.Text(
                                        video_title,
                                        td="none",
                                        fw=500,
                                        mb="5px",
                                        c="var(--mantine-color-text)",
                                        size="sm",
                                    ),
                                    dmc.Text(
                                        dmc.Anchor(
                                            videotype_name,
                                            href=get_search_link(category_id, type_id),
                                            className="video-link",
                                            underline='always'
                                        ),
                                        c="gray",
                                        td="none",
                                        size="sm",
                                    ),
                                    dmc.Group(
                                        [
                                            dmc.Text(
                                                date,
                                                c="gray",
                                                td="none",
                                                size="sm",
                                            ),
                                        ],
                                        gap="xs",
                                    ),
                                ],
                                mt="3px",
                                ml="10px",
                                p=0,
                            ),
                        ],
                    ),
                ],
            )
        ],
    )


def create_video_miniatures_container(children):
    """
    Функция createVideoMiniaturesContainer создает контейнер для видео миниатюр.

    :param children:
    :return dmc.Flex:
    """
    return dmc.Flex(
        direction="row",
        wrap="wrap",
        justify="space-around",
        children=children,
        mx='xs'
    )


def create_video_search_bar(
    page, search_clicks=0, input_value=None, additional_children=None
):
    """
    Функция createVideoSearchBar создает строку поиска видео.

    :param page:
    :param search_clicks:
    :param input_value:
    :param additional_children:
    :return dmc.Grid: экземпляр класса dmc.Grid с заданными параметрами и дочерними элементами.
    """

    if additional_children is None:
        additional_children = [html.Div()]
    search_form = dmc.Group(
        [
            dmc.TextInput(
                placeholder="Введите запрос",
                value=input_value,
                id="n_search_query_video",
                name="query",
                rightSection=[
                    dmc.Button(
                        "Поиск",
                        id="n_search_button_video",
                        n_clicks=search_clicks,
                    )
                ],
                rightSectionWidth='max-content',
                w='100%'
            ),
            dmc.TextInput(display="none", value="y", name="l"),
            dmc.TextInput(display="none", value="y", name="auto_search"),
        ],
        justify="center",
        wrap="nowrap",
        mx='xs'
    )

    return dmc.Grid(
        [
            dmc.GridCol(span=3, display={'base': 'none', 'md': 'block'}),  
            dmc.GridCol(
                span="auto",
                children=dmc.Stack(
                    [
                        (
                            html.Form(search_form, action="/players/video/search")
                            if page == "main"
                            else search_form
                        )
                    ] +
                    additional_children,
                    gap="xs",
                ),
            ),
            dmc.GridCol(span=3, display={'base': 'none', 'md': 'block'}),
        ],
        w="90%",
        m="auto",
    )


def get_random_videos(conn, counter=28, type_id=None):
    """

    :param conn: db connection to PostgreSQL
    :param counter:
    :param type_id:
    :return:
    """
    if type_id is not None:
        query = "select * from filestorage_mediafiles_summary where html_video_ready and type_id = %(type_id)s order by random() limit %(counter)s;"
    else:
        query = "select * from filestorage_mediafiles_summary where html_video_ready order by random() limit %(counter)s;"

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            {"counter": counter, "type_id": type_id},
        )

        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data
