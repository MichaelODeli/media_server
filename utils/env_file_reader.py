import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def get_env_value(key_name):
    """

    :param key_name:
    :return:
    """
    try:
        key_value = os.environ.get(key_name)
        return key_value
    except Exception:
        return None
