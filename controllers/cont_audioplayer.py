from psycopg2.extensions import AsIs


def get_audio_types(conn, type_id=None):
    """

    :param conn: db connection to PostgreSQL
    :param type_id: audio type_id (default: None)
    :return: dict with audio info
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """select * from (select distinct(type_id) from filestorage_mediafiles_summary fms where html_audio_ready)
                left join (select id as type_id, type_name from filestorage_types) ft using(type_id) %(addition)s;""",
            {"addition": AsIs(f"WHERE type_id = {type_id}" if type_id else "")},
        )

        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data


def get_audio_dict(conn, type_id):
    """

    :param conn: db connection to PostgreSQL
    :param type_id: audio type_id (default: None)
    :return: dict with audio info
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """select * from filestorage_mediafiles_summary fms WHERE html_audio_ready and type_id = %(type_id)s order by artist, audio_title;""",
            {"type_id": type_id},
        )

        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data
