def get_header_links(conn):
    """

    :param conn: db connection to PostgreSQL
    :return (dict): header links
    """
    with conn.cursor() as cursor:
        cursor.execute("select * from header_links;")
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data
