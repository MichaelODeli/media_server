import hashlib
import mimetypes
import os
import traceback

import cv2 as cv
import mutagen
from psycopg2.extensions import AsIs

FORBIDDEN_FIRST_SYMBOLS = ["_", "-", "."]


def define_mime_type(conn, fileway):
    """

    :param conn: db connection to PostgreSQL
    :param fileway:
    :return:
    """
    mime = mimetypes.guess_type(fileway)
    if mime[0] is None:
        with conn.cursor() as cursor:
            cursor.execute(
                f"select type_name from mime_types_secondary mts where extension like '%{fileway.split('.')[-1]}%';"
            )
            result = cursor.fetchone()
            return result[0] if result is not None else "unknown/unknown"
    else:
        return mime[0]


def video_properties_with_open_cv(media_fullway):
    """
    Функция videoDurationWithOpenCV получает длительность видеофайла с помощью библиотеки OpenCV.
    Если видеофайл невалидный, функция возвращает -1.

    :param media_fullway: путь к видеофайлу
    :return: длительность видеофайла в секундах и число кадров в секунду
    """
    video = cv.VideoCapture(media_fullway)
    if not video.isOpened():
        # need to catch errors
        duration, fps, width, height = [0] * 4
        fps = 0
    else:
        fps = video.get(cv.CAP_PROP_FPS)
        frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        duration = int(frame_count / fps)
        width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))  # float `width`
        height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))  # float `height`
    return duration, fps, height, width


def audio_properties_with_mutagen(media_fullway):
    """
    Функция audioPropertiesWithMutagen получает свойства аудиофайла с помощью библиотеки Mutagen.
    Если аудиофайл невалидный, функция возвращает None.

    :param media_fullway: путь к аудиофайлу
    :return: словарь свойств аудиофайла
    """

    data = {
        "audio_duration": 0,
        "audio_bitrate": "NULL",
        "audio_samplerate": "NULL",
        "audio_artist": "NULL",
        "audio_title": "NULL",
        "audio_album_title": "NULL",
        "audio_year": "NULL",
        "audio_genre": "NULL",
    }

    try:
        audiofile = mutagen.File(media_fullway)
        data["audio_duration"] = int(audiofile.info.length)
        data["audio_bitrate"] = int(audiofile.info.bitrate)
        data["audio_samplerate"] = int(audiofile.info.sample_rate) / 1000

        data["audio_artist"] = (
            "'" + audiofile.tags["TPE1"].text[0] + "'"
            if "TPE1" in audiofile.keys()
            else "NULL"
        )
        data["audio_title"] = (
            "'" + audiofile.tags["TIT2"].text[0] + "'"
            if "TIT2" in audiofile.keys()
            else "NULL"
        )
        data["audio_album_title"] = (
            "'" + audiofile.tags["TALB"].text[0] + "'"
            if "TALB" in audiofile.keys()
            else "NULL"
        )
        data["audio_year"] = (
            audiofile.tags["TDRC"].text[0] if "TDRC" in audiofile.keys() else "NULL"
        )
        data["audio_genre"] = (
            "'" + audiofile.tags["TCON"].text[0] + "'"
            if "TCON" in audiofile.keys()
            else "NULL"
        )
    except Exception:
        pass
    finally:
        return data


# вставка
def insert_mime(mime_name, conn) -> dict:
    """
    Функция insertMIME принимает на вход имя MIME-типа и возвращает его описание.
    Если запись с таким именем MIME-типа отсутствует в базе данных, она создает новую запись.
    В противном случае функция возвращает уже существующую запись.

    :param mime_name: имя MIME-типа
    :param conn: db connection to PostgreSQL
    :return: описание MIME-типа:
    {secondary_mime_id, primary_mime_id, type_name, is_audio, is_video, html_video_ready, html_audio_ready, search_enabled}
    """
    # conn = db_connection.getConn()
    with conn.cursor() as cursor:
        # conn.autocommit = True

        cursor.execute(
            f"select count(*) FROM mime_types_secondary where type_name = '{mime_name}';"
        )
        counter = cursor.fetchone()[0]
        if counter > 0:
            pass
        else:
            primary_mime_name = mime_name.split("/")[0]
            cursor.execute(
                f"select id FROM mime_types_primary where type_name = '{primary_mime_name}';"
            )
            primary_mime_id = cursor.fetchone()[0]
            cursor.execute(
                f"INSERT INTO mime_types_secondary (type_name, primary_mime_id) VALUES ('{mime_name}', {primary_mime_id});"
            )

        cursor.execute(
            f"""SELECT id as secondary_mime_id, primary_mime_id,
            type_name, is_audio, is_video, html_video_ready,
            html_audio_ready, search_enabled
            FROM mime_types_secondary where type_name = '{mime_name}';"""
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()][0]
    return data


# получение данных из БД
def get_baseway(conn, test: bool = True):
    """
    Функция getBaseway возвращает базовый путь в библиотеке.
    Если параметр test равен True, функция выполняет запрос к базе данных с тестовым значением.
    Если параметр test равен False, функция выполняет запрос к базе данных с реальным значением.
    Если директория, указанная в результате запроса, существует, функция возвращает эту директорию.
    В противном случае функция вызывает исключение NotADirectoryError с сообщением 'Директория не найдена'.

    :param conn: db connection to PostgreSQL
    :param test: флаг, указывающий на использование тестового значения (по умолчанию True)
    :return: базовый путь в библиотеке
    :raises NotADirectoryError: если директория, указанная в результате запроса, не существует
    """
    # conn = db_connection.getConn()
    with conn.cursor() as cursor:
        cursor.execute(
            f"select parameter_value FROM config where parameter_name = 'filemanager.baseway' and test_value = '{test}';"
        )
        result = cursor.fetchone()[0]

    if test:
        return result
    else:
        if os.path.exists(result):
            return result
        else:
            raise NotADirectoryError("Директория не найдена")


def get_settings(conn):
    """

    :param conn: db connection to PostgreSQL
    :return:
    """
    with conn.cursor() as cursor:
        cursor.execute("select * FROM config;")
        data = cursor.fetchall()

        return {(i[1] if i[3] is False else i[1] + ".test"): i[2] for i in data}


def get_categories(conn, category_id=None):
    """
    Функция getCategories получает категории из базы данных и добавляет к каждой категории ее актуальный путь.
    Актуальный путь рассчитывается путем объединения базового пути библиотеки с путем категории.
    Если путь категории является абсолютным, он остается неизменным.
    Если в базе данных нет категорий, функция возвращает None.

    :param conn: db connection to PostgreSQL
    :param category_id: идентификатор категории. Если None, то выбираются все категории.
    :return: список категорий с актуальными путями или None, если категорий нет в базе данных
    """
    baseway = get_baseway(conn)
    # conn = db_connection.getConn()

    # select categories
    with conn.cursor() as cursor:
        addition = (
            f"where id = {category_id}" if category_id is not None else "where active"
        )
        cursor.execute(
            f"select id as category_id, way, category_name, category_pseudonym, is_absolute_way, main_mime_type_id from filestorage_categories {addition} order by category_name;"
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    # add actual way
    if len(data) > 0:
        for i in range(len(data)):
            full_way = (
                (baseway + data[i]["way"])
                if not data[i]["is_absolute_way"]
                else data[i]["way"]
            )
            data[i]["full_way"] = full_way
        return data
    else:
        return []


def get_types(conn, category_id, type_id=None):
    """
    Функция getTypes получает типы из базы данных и добавляет к каждому типу его актуальный путь.
    Актуальный путь рассчитывается путем объединения базового пути библиотеки с путем типа.
    Если путь типа является абсолютным, он остается неизменным.
    Если в базе данных нет типов, функция возвращает None.

    :param type_id:
    :param conn: db connection to PostgreSQL
    :param category_id: идентификатор категории.
    :return: список типов с актуальными путями или None, если типов нет в базе данных
    """
    # conn = db_connection.getConn()

    # select categories
    with conn.cursor() as cursor:
        addition = f"and id = {type_id}" if type_id is not None else "and active"
        cursor.execute(
            f"""select id as type_id, category_id, way, type_name, type_pseudonym, is_absolute_way 
            from filestorage_types where category_id = {category_id} {addition} order by type_name;"""  # noqa: W291
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    # add actual way
    if len(data) > 0:
        category_way = get_categories(conn, category_id=category_id)[0]["full_way"]
        for i in range(len(data)):
            full_way = (
                (category_way + data[i]["way"])
                if not data[i]["is_absolute_way"]
                else data[i]["way"]
            )
            data[i]["full_way"] = full_way
        return data
    else:
        return []


def get_files(conn, category_id, type_id, file_id=None):
    """
    Функция getFiles получает файлы из базы данных и добавляет к каждому файлу его полный путь.
    Полный путь рассчитывается путем объединения пути типа с путем файла.
    Если путь файла является абсолютным, он остается неизменным.
    Если в базе данных нет файлов, функция возвращает None.

    :param conn: db connection to PostgreSQL
    :param category_id: идентификатор категории
    :param type_id: идентификатор типа
    :param file_id: идентификатор файла. Если None, то выбираются все файлы.
    :return: список файлов с полными путями или None, если файлов нет в базе данных
    """
    with conn.cursor() as cursor:
        addition = f"and id = {file_id}" if file_id is not None else ""
        cursor.execute(
            f"""select encode(id, 'hex') as file_id, type_id, way, filename, is_absolute_way, mime_type_id, size_kb
            from filestorage_files where type_id = {type_id} {addition};"""
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    # add actual way
    if len(data) > 0:
        type_way = get_types(conn, category_id=category_id, type_id=type_id)[0][
            "full_way"
        ]
        for i in range(len(data)):
            full_way = (
                (type_way + data[i]["way"] + data[i]["filename"])
                if not data[i]["is_absolute_way"]
                else data[i]["way"] + data[i]["filename"]
            )
            data[i]["full_way"] = full_way
        return data
    else:
        return []


# Обновление Mime-типа для категории/типа
def update_mime_on_categories_types(conn):
    """
    Функция updateMIMEonCategoriesTypes обновляет основные MIME-типы для категорий и типов в базе данных.
    Она получает основные MIME-типы из таблицы mime_types_secondary и обновляет соответствующие поля в таблицах filestorage_categories и filestorage_types.

    :param conn: db connection to PostgreSQL
    :return: None
    """
    with conn.cursor() as cursor:
        for category in get_categories(conn):
            category_id = category["category_id"]
            cursor.execute(
                f"select mime_type_id from filestorage_mimes_categories_summary where category_id = {category_id}"
            )
            result = cursor.fetchone()

            if result is not None:
                mime_type_id_secondary = result[0]
                cursor.execute(
                    f"select primary_mime_id from mime_types_secondary where id = {mime_type_id_secondary}"
                )
                mime_type_id_primary = cursor.fetchone()[0]

                print(category["category_name"], mime_type_id_primary)

                cursor.execute(
                    f"UPDATE filestorage_categories SET main_mime_type_id = {mime_type_id_primary} WHERE id = {category_id};"
                )
            else:
                pass
            for types in get_types(conn, category_id=category_id):
                type_id = types["type_id"]
                cursor.execute(
                    f"select mime_type_id from filestorage_mimes_types_summary where type_id = {type_id}"
                )
                result = cursor.fetchone()

                if result is not None:
                    mime_type_id_secondary = result[0]
                    cursor.execute(
                        f"select primary_mime_id from mime_types_secondary where id = {mime_type_id_secondary}"
                    )
                    mime_type_id_primary = cursor.fetchone()[0]

                    print(types["type_name"], mime_type_id_primary)

                    cursor.execute(
                        f"UPDATE filestorage_types SET main_mime_type_id = {mime_type_id_primary} WHERE id = {type_id};"
                    )
                else:
                    pass


# парсинг
def parse_categories(
    conn, reset: bool = False, add_new: bool = False, scan_exists: bool = True
):
    """
    Функция parseCategories проверяет наличие категорий в базе данных и обновляет их, если необходимо.
    Если параметр reset равен True, функция удаляет все категории из базы данных и добавляет их заново.
    Если параметр reset равен False, функция проверяет наличие категорий в базе данных и удаляет те, которые отсутствуют на диске.
    Функция возвращает список категорий после обновления.

    :param add_new:
    :param scan_exists:
    :param conn: db connection to PostgreSQL
    :param reset: флаг, указывающий на необходимость полного обновления категорий (по умолчанию False)
    :return: список категорий после обновления
    """
    baseway = get_baseway(conn)
    global FORBIDDEN_FIRST_SYMBOLS
    # conn = db_connection.getConn()

    # verify exist categories
    with conn.cursor() as cursor:
        # conn.autocommit = True
        if reset:
            print("drop trigger")
            cursor.execute("DELETE FROM filestorage_categories;")
        else:
            if scan_exists:
                # get all categories from database
                data = get_categories(conn)

                # verify existing categories from database
                non_exist_categories = (
                    [
                        f["category_id"]
                        for f in data
                        if not os.path.exists(f["full_way"])
                    ]
                    if data is not None
                    else []
                )

                # delete non exist categories from database
                if len(non_exist_categories) > 0:
                    for c_id in non_exist_categories:
                        cursor.execute(
                            f"delete from filestorage_categories where id = {c_id};"
                        )

        # add categories
        if add_new:
            conflict_addition = "ON CONFLICT (category_name) DO NOTHING"
            dirs = [
                f
                for f in os.listdir(baseway)
                if (
                    (os.path.isdir(baseway + f) or os.path.islink(baseway + f))
                    and f[0] not in FORBIDDEN_FIRST_SYMBOLS
                )
            ]

            commands = [
                f"INSERT INTO filestorage_categories (category_name, way) VALUES ('{i}', '{i + '/'}') {conflict_addition};"
                for i in dirs
            ]
            for command in commands:
                cursor.execute(command)

    return get_categories(conn)


def parse_types(conn, category_id, reset=False, add_new=False, scan_exists=True):
    """
    Функция parseTypes выполняет парсинг типов из базы данных и удаляет не существующие типы.

    :param add_new:
    :param scan_exists:
    :param conn: db connection to PostgreSQL
    :param category_id: идентификатор категории.
    :param reset: Если True, то все типы и категории будут удалены из базы данных. По умолчанию False.

    :return: список типов категории после парсинга или None, если типов нет в базе данных
    """

    global FORBIDDEN_FIRST_SYMBOLS

    with conn.cursor() as cursor:
        # conn.autocommit = True
        if reset:
            cursor.execute(
                f"DELETE FROM filestorage_types where category_id = {category_id};"
            )
        else:
            if scan_exists:
                for category in get_categories(conn, category_id=category_id):
                    # get all types from database

                    data = get_types(conn, category_id=category_id)

                    # verify existing files from database
                    non_exist_types = (
                        [
                            f["type_id"]
                            for f in data
                            if not os.path.exists(f["full_way"])
                        ]
                        if data is not None
                        else []
                    )

                if len(non_exist_types) > 0:
                    for t_id in non_exist_types:
                        cursor.execute(
                            f"delete from filestorage_types where id = {t_id};"
                        )

        # add types
        if add_new:
            for category in get_categories(conn, category_id=category_id):
                category_id = category["category_id"]
                category_way = category["full_way"]
                conflict_addition = "ON CONFLICT (category_id, type_name) DO NOTHING"
                dirs = [
                    f
                    for f in os.listdir(category_way)
                    if (
                        os.path.isdir(category_way + f)
                        or os.path.islink(category_way + f)  # noqa: W503
                    )
                    and f[0] not in FORBIDDEN_FIRST_SYMBOLS
                ]

                commands = [
                    f"INSERT INTO filestorage_types (category_id, type_name, way) VALUES ({category_id}, $${i}$$, $${i + '/'}$$) {conflict_addition};"
                    for i in dirs
                ]
                for command in commands:
                    cursor.execute(command)

    return get_types(conn, category_id)


def parse_files(conn, category_id, type_id, reset=False):
    """
    Функция parseFiles выполняет парсинг файлов из базы данных и удаляет не существующие файлы.

    :param conn: db connection to PostgreSQL
    :param category_id: идентификатор категории
    :param type_id: идентификатор типа
    :param reset: Если True, то все файлы и типы будут удалены из базы данных. По умолчанию False.

    :return: список файлов категории после парсинга или None, если файлов нет в базе данных
    """

    global FORBIDDEN_FIRST_SYMBOLS

    with conn.cursor() as cursor:
        # conn.autocommit = True
        if not reset:
            for types in get_types(conn, category_id=category_id, type_id=type_id):
                # get all types from database
                data = get_files(conn, category_id=category_id, type_id=type_id)

                # verify existing files from database
                hashes = [f["file_id"] for f in data] if data is not None else []
                non_exist_files = (
                    [f["file_id"] for f in data if not os.path.exists(f["full_way"])]
                    if data is not None
                    else []
                )

            if len(non_exist_files) > 0:
                for f_id in non_exist_files:
                    cursor.execute(
                        f"delete from filestorage_files where id = decode('{f_id}', 'hex');"
                    )
        else:
            hashes = []
            non_exist_files = []
            cursor.execute(f"DELETE FROM filestorage_files where type_id = {type_id};")

        # add files
        for types in get_types(conn, category_id=category_id, type_id=type_id):
            type_id = types["type_id"]
            type_way = types["full_way"][:-1]

            # with conn.cursor() as cursor:
            for root, dirs, files in os.walk(type_way):
                if root[len(type_way) :].count(os.sep) <= int(
                    get_settings(conn)["filemanager.depth"]
                ):
                    data = []
                    media_commands = []
                    root = root.replace("\\", "/")
                    way = root.replace(type_way, "") + "/"

                    for file in files:
                        full_way = type_way + way + file

                        if any(
                            [
                                i[0] in FORBIDDEN_FIRST_SYMBOLS
                                for i in full_way.split("/")
                            ]
                        ):
                            continue
                        else:
                            # with open(full_way, "rb") as f:
                            #     hash_file = hashlib.file_digest(f, "sha256")
                            hash_file = hashlib.sha256(
                                bytes(full_way, encoding="UTF-8")
                            ).hexdigest()

                            if hash_file in hashes:
                                continue
                            else:
                                mime_info = insert_mime(
                                    define_mime_type(conn, full_way), conn
                                )

                                primary_mime = mime_info["type_name"].split("/")[0]
                                if primary_mime in ["video", "audio"]:
                                    table_name = f"filestorage_mediainfo_{primary_mime}"
                                    if primary_mime == "video":
                                        values_name = (
                                            "file_id, duration, fps, height, width"
                                        )
                                        video_info = video_properties_with_open_cv(
                                            full_way
                                        )
                                        values_media = f"decode('{hash_file}', 'hex'), {float(video_info[0])}, {int(video_info[1])}, {int(video_info[2])}, {int(video_info[3])}"
                                    elif primary_mime == "audio":
                                        # print(full_way)
                                        values_name = 'file_id, duration, bitrate, sample_rate, artist, audio_title, album_title, "year", genre'
                                        audio_info = audio_properties_with_mutagen(
                                            full_way
                                        )
                                        # values_media = "decode('{}', 'hex'), {}, {}, {}, '{}', '{}', '{}', {}, '{}'".format(
                                        values_media = "decode('{}', 'hex'), {}, {}, {}, $${}$$, $${}$$, $${}$$, {}, $${}$$".format(
                                            hash_file,
                                            audio_info["audio_duration"],
                                            audio_info["audio_bitrate"],
                                            audio_info["audio_samplerate"],
                                            audio_info["audio_artist"],
                                            audio_info["audio_title"],
                                            audio_info["audio_album_title"],
                                            audio_info["audio_year"],
                                            audio_info["audio_genre"],
                                        )
                                    else:
                                        pass

                                    media_commands.append(
                                        f"INSERT INTO {table_name} ({values_name}) VALUES ({values_media});"
                                    )

                                data.append(
                                    {
                                        "way": way[1:],
                                        "filename": file,
                                        "type_id": type_id,
                                        "id": hash_file,
                                        "mime_type_id": mime_info["secondary_mime_id"],
                                        "size_kb": int(
                                            os.path.getsize(full_way) / 1024
                                        ),
                                    }
                                )
                    commands = [
                        "INSERT INTO filestorage_files (id, type_id, way, filename, mime_type_id, size_kb) "
                        f"VALUES (decode('{i['id']}', 'hex'), {type_id}, $${i['way']}$$, $${i['filename']}$$, {i['mime_type_id']}, {i['size_kb']});"
                        for i in data
                    ]

                    # выполнение команд на добавление файлов
                    counter = 0
                    for command in commands:
                        try:
                            counter += 1
                            cursor.execute(command)
                        except Exception:
                            print(traceback.format_exc())
                            print(command)

                    # выполнение команд на добавление информации к медиафайлам
                    for media_command in media_commands:
                        try:
                            cursor.execute(media_command)
                        except Exception:
                            print(traceback.format_exc())
                            print(media_command)

    return get_files(conn, category_id, type_id), counter, len(non_exist_files)


def parse(conn, mode="update_files"):
    """
    Функция parse выполняет парсинг категорий, типов и файлов из базы данных.

    :param conn: db connection to PostgreSQL
    :param mode: режим парсинга. Допустимые значения: "update_files", "update_types", "update_categories", "reset".
    :return: None
    """

    if mode not in ["update_files", "update_types", "update_categories", "reset"]:
        raise ValueError("Неверно указан режим или тип парсинга")

    update_categories = False
    update_types = False
    update_files = False
    reset = False

    if mode == "update_categories":
        update_categories = True
    elif mode == "update_types":
        update_types = True
    elif mode == "update_files":
        update_files = True
    else:
        input("Confirm reset")
        update_categories = True
        update_types = True
        update_files = True
        reset = True

    for category in parse_categories(conn, reset=reset, add_new=update_categories):
        result = parse_types(
            conn, category_id=category["category_id"], reset=reset, add_new=update_types
        )
        print(
            f"found category {category['category_name']} (id: {category['category_id']})"
        )

        if update_types or update_files or reset:
            print(f"--- in {category['category_name']} found {len(result)} types")
            for types in result:
                print(
                    f"------ found type {types['type_name']} (id: {types['type_id']})"
                )
                if update_files or reset:
                    files_result = parse_files(
                        conn,
                        category_id=category["category_id"],
                        type_id=types["type_id"],
                        reset=reset,
                    )
                    if files_result[0] is not None:
                        print(
                            f"--------- in {types['type_name']} found {len(files_result[0])} files. "
                            f"New files: {files_result[1]}. "
                            f"Removed {files_result[2]} files."
                        )

    if reset:
        update_mime_on_categories_types(conn)


def get_file_info(conn, file_id):
    """
    Функция getFileInfo выполняет получение информации о файле из базы данных.

    :param conn: db connection to PostgreSQL
    :param file_id: идентификатор файла
    :return: словарь с описанием файла
    """
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM filestorage_files_summary where file_id = %(file_id)s;",
            {"file_id": file_id},
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

        return data


def get_filesearch_result(
    conn,
    mode,
    query="",
    limit=50,
    offset=0,
    categories=None,
    types=None,
    table_name="filestorage_files_summary",
    from_video=False,
):
    """
    Функция getFilesearchResult получает результаты поиска файлов в базе данных.

    :param from_video:
    :param conn: db connection to PostgreSQL
    :param query: поисковый запрос
    :param mode: режим поиска. Допустимые значения: "all", "by_category", "all_from_category", "all_from_category_type", "by_category_type_query".
    :param limit: количество результатов на странице
    :param offset: смещение
    :param categories: список категорий
    :param types: список типов
    :param columns_names: имена столбцов для выборки
    :param table_name: имя таблицы в базе данных
    :return: количество результатов и список результатов поиска
    """

    if categories is None:
        categories = []
    if types is None:
        types = []
    table_name = (
        "filestorage_mediafiles_summary" if from_video else "filestorage_files_summary"
    )
    if mode == "all":
        where_addition = "LOWER(file_name) LIKE LOWER(%(query)s)"
    elif mode == "by_category":
        where_addition = (
            "LOWER(file_name) LIKE LOWER(%(query)s) and category_id in (%(categories)s)"
        )
    elif mode == "all_from_category":
        where_addition = "category_id in (%(categories)s)"
    elif mode == "all_from_category_type":
        where_addition = "category_id in (%(categories)s) and type_id in (%(types)s)"
    elif mode == "by_category_type_query":
        where_addition = "LOWER(file_name) LIKE LOWER(%(query)s) and category_id in (%(categories)s) and type_id in (%(types)s)"
    else:
        raise TypeError("Неверный режим")

    with conn.cursor() as cursor:
        if from_video:
            where_addition += " and html_video_ready"

        cursor.execute(
            "SELECT %(what)s FROM %(table_name)s WHERE {};".format(where_addition),
            {
                "what": AsIs("count(*)"),
                "table_name": AsIs(table_name),
                "query": "%%" + query + "%%",
                "categories": AsIs(", ".join(categories)),
                "types": AsIs(", ".join(types)),
            },
        )

        count_results = cursor.fetchone()[0]

        if count_results > 0:
            cursor.execute(
                "SELECT * FROM %(table_name)s WHERE {} order by category_name asc, type_name asc, file_name asc LIMIT %(limit)s OFFSET %(offset)s;".format(
                    where_addition
                ),
                {
                    "table_name": AsIs(table_name),
                    "query": "%%" + query + "%%",
                    "categories": AsIs(", ".join(categories)),
                    "types": AsIs(", ".join(types)),
                    "limit": limit,
                    "offset": offset,
                },
            )

            desc = cursor.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        else:
            data = []

        return count_results, data


def generate_thubmnails():
    """ """
    raise NotImplementedError
