import dash_mantine_components as dmc
from dash import Input, Output, State, callback, html, no_update, register_page
from flask import request

from controllers import cont_search, cont_video, db_connection
from controllers import service_controller as service

register_page(__name__, path="/players/video/search", icon="fa-solid:home")

query_global = ""


def layout(
    l="n",
    query="",
    category_id=None,
    type_id=None,
    auto_search="n",
    **other_unknown_query_strings,
):
    """

    :param l:
    :param query:
    :param category_id:
    :param type_id:
    :param auto_search:
    :param other_unknown_query_strings:
    :return:
    """
    if category_id is None:
        category_id = []
    if type_id is None:
        type_id = []
    service.log_printer(request.remote_addr, "videosearch", "page opened")
    if l == "n":
        return dmc.Container()
    else:
        global query_global
        query_global = query

        conn = db_connection.get_conn()

        category_id, type_id = cont_search.format_category_type(category_id, type_id)

        category_select_data = cont_search.get_categories_for_multi_select(conn, video=True)

        if auto_search != "n" and (query != "" or category_id != []):
            search_clicks = 1
        else:
            search_clicks = 0

        return dmc.Stack(
            id="dummy-1",
            pt="20px",
            gap="xs",
            children=[
                cont_video.create_video_search_bar(
                    page="search",
                    input_value=query,
                    additional_children=[
                        cont_search.get_search_accordion(
                            category_id, type_id, category_select_data, from_video=True
                        )
                    ],
                    search_clicks=search_clicks,
                ),
                html.Div(id="search_results_video"),
                dmc.Center(
                    dmc.Pagination(
                        total=1,
                        value=1,
                        siblings=1,
                        withControls=True,
                        withEdges=True,
                        id="search_pagination_video",
                    ),
                    py='xs',
                    w='100%'
                ),
            ],
        )


cont_search.get_types_addition_format_callback(from_video=True)


@callback(
    Output("search_results_video", "children"),
    Output("search_pagination_video", "total"),
    Input("search_pagination_video", "value"),
    Input("n_search_button_video", "n_clicks"),
    State("n_search_in_category_video", "value"),
    State("n_search_in_types_video", "value"),
    State("n_search_query_video", "value"),
)
def get_video_search_results(current_page, n_clicks, categories, types, query):
    """

    :param current_page:
    :param n_clicks:
    :param categories:
    :param types:
    :param query:
    :return:
    """
    if n_clicks == 0:
        return html.Center([dmc.Title("Пустой поисковый запрос. Повторите снова.", order=4)]), 1
    else:
        global query_global
        query_global = query

        conn = db_connection.get_conn()
        current_page -= 1

        page_limit = cont_search.PAGE_LIMIT_VIDEO
        offset = current_page * page_limit

        counter, query_results = cont_search.get_search_results(
            conn,
            query,
            categories,
            types,
            limit=page_limit,
            offset=offset,
            from_video=True,
        )

        if counter == -1:
            return no_update, 1
        elif counter == -2:
            return "Ошибочка", 1
        elif counter == 0:
            return html.Center(dmc.Title("По Вашему запросу результатов нет", order=4)), 1
        else:
            pages = (
                int(counter / page_limit) + 1
                if counter % page_limit != 0
                else counter / page_limit
            )

            return (
                cont_video.create_video_miniatures_container(
                    children=[
                        cont_video.create_video_miniature_container(
                            href=f"/players/video/watch?v={video['file_id']}&l=y",
                            video_title=cont_search.string_hider(
                                ".".join(video["file_name"].split(".")[:-1])
                            ),
                            videotype_name=cont_search.string_hider(video["type_name"]),
                            video_duration=video["video_duration"],
                            date=service.get_date_difference(video["created_at"]),
                            category_id=video["category_id"],
                            type_id=video["type_id"],
                        )
                        for video in query_results
                    ]
                ),
                pages,
            )
