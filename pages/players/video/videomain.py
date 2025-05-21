import dash_mantine_components as dmc
from dash import register_page
from flask import request

from controllers import cont_search, cont_video, db_connection
from controllers import service_controller as service

register_page(__name__, path="/players/video", icon="fa-solid:home")


def layout(l="n", **other_unknown_query_strings):  # noqa: E741
    """

    :param l:
    :param other_unknown_query_strings:
    :return:
    """
    service.log_printer(request.remote_addr, "videomain", "page opened")
    if l == "n":
        return dmc.Container()
    else:
        conn = db_connection.get_conn()

        return dmc.Stack(
            pt="20px",
            gap="xs",
            children=[
                # cont_video.createVideoSearchBar(page="main"),
                cont_video.create_video_miniatures_container(
                    children=[
                        cont_video.create_video_miniature_container(
                            href=f"/players/video/watch?v={video['file_id']}&l=y",
                            video_title=cont_search.string_hider(
                                ".".join(video["file_name"].split(".")[:-1])
                            ),
                            videotype_name=video["type_name"],
                            video_duration=video["video_duration"],
                            date=service.get_date_difference(video["created_at"]),
                            category_id=video["category_id"],
                            type_id=video["type_id"],
                        )
                        for video in cont_video.get_random_videos(conn)
                    ],
                ),
            ],
        )
