import os

import psycopg2
from dotenv import dotenv_values

# load environment variables
config = {
    **dotenv_values("./.env"),
    # **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

DBNAME = config['DB_NAME']
USER = config['DB_USER']
PASSWORD = config['DB_PASSWORD']
HOST = config['DB_HOST_LOCAL'] if not os.environ.get("AM_I_IN_A_DOCKER_CONTAINER", False) else config['DB_HOST_DOCKER']
PORT = int(config['DB_PORT'])


def test_conn(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT):
    """
    Функция testConn проверяет соединение с базой данных.

    :param dbname: имя базы данных.
    :param user: имя пользователя базы данных.
    :param password: пароль пользователя базы данных.
    :param host: хост базы данных.
    :param port: порт базы данных.
    :return: True, если соединение установлено успешно, иначе False.
    """
    try:
        """
        Пытается установить соединение с базой данных.
        """
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        """
        Закрывает соединение с базой данных.
        """
        conn.close()
        return True
    except Exception:
        """
        Если возникает ошибка при установке соединения, функция возвращает False.
        """
        return False


def get_conn(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT):
    """
    Функция getConn возвращает соединение с базой данных, если оно установлено успешно, иначе None.

    :param dbname: имя базы данных.
    :param user: имя пользователя базы данных.
    :param password: пароль пользователя базы данных.
    :param host: хост базы данных.
    :param port: порт базы данных.
    :return: соединение с базой данных, если оно установлено успешно, иначе None.
    """
    if test_conn():
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        conn.autocommit = True
        return conn
    else:
        return psycopg2.errors.ConnectionFailure('Сервер недоступен.')
