import time


def get_duration(seconds_data: float):
    """
    Преобразует количество секунд в формат времени HH:MM:SS.

    :param (float) seconds_data: Количество секунд.
    :return str: Строка в формате HH:MM:SS, представляющая время.
    """
    if seconds_data < 3600:
        time_format = "%M:%S"
    else:
        time_format = "%H:%M:%S"
    return time.strftime(time_format, time.gmtime(float(seconds_data)))
