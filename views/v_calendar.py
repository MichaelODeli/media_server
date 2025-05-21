import calendar
from datetime import datetime

import dash_mantine_components as dmc


def render_mini_calendar():
    """

    :return:
    """
    cal = calendar.Calendar()
    week_days_name = calendar.weekheader(2).split(" ")

    mini_calendar = dmc.Table(
        [
            dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh(
                            dmc.Text(
                                week_days_name[week_day_number],
                                size="xs",
                                c="red" if week_day_number in [5, 6] else "inerhit",
                            ),
                            className="center-content-horizontal w-content",
                            p=2,
                        )
                        for week_day_number in range(7)
                    ]
                )
            ),
            dmc.TableTbody(
                [
                    dmc.TableTr(
                        [
                            dmc.TableTd(
                                dmc.Indicator(
                                    [
                                        dmc.ActionIcon(
                                            dmc.Text(
                                                week_day.day,
                                                c=(
                                                    "dimmed"
                                                    if week_day.month
                                                    != datetime.now().month
                                                    else "inerhit"
                                                ),
                                            ),
                                            radius="xl",
                                            variant=(
                                                "default"
                                                if week_day.day != datetime.now().day
                                                else "filled"
                                            ),
                                            className="border-0",
                                        )
                                    ],
                                    position="bottom-center",
                                    disabled=(
                                        False
                                        if week_day.day == datetime.now().day + 1
                                        else True
                                    ),
                                    # w="max-content",
                                ),
                                className="center-content-horizontal w-content",
                                p=2,
                            )
                            for week_day in week_days
                        ]
                    )
                    for week_days in cal.monthdatescalendar(
                        datetime.now().year, datetime.now().month
                    )
                ]
            ),
        ],
        withRowBorders=False,
        # w="max-content",
        mx="auto",
    )

    return mini_calendar


def render_plans_navbar():
    """

    :return:
    """
    plans_timeline = dmc.Timeline(
        ps="md",
        active=-1,
        bulletSize=15,
        lineWidth=2,
        children=[
            dmc.TimelineItem(
                title="Сделать то-то",
                children=dmc.Stack(
                    [
                        dmc.Text(
                            "Время выполнения: 10:08 11/09/2024",
                            size="sm",
                            c="dimmed",
                        ),
                        dmc.Anchor(
                            "Посмотреть задачу",
                            href="#",
                            size="sm",
                        ),
                    ],
                    gap=0,
                ),
            )
        ]
        * 4,
    )
    return plans_timeline


def render_maxi_calendar():
    """

    :return:
    """
    cal = calendar.Calendar()
    week_days_name = calendar.weekheader(2).split(" ")

    maxi_calendar = dmc.Table(
        [
            dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh(
                            dmc.Text(
                                week_days_name[week_day_number],
                                size="md",
                                c="red" if week_day_number in [5, 6] else "inerhit",
                            ),
                            className="center-content-horizontal w-content",
                            p=5,
                        )
                        for week_day_number in range(7)
                    ]
                )
            ),
            dmc.TableTbody(
                [
                    dmc.TableTr(
                        [
                            dmc.TableTd(
                                dmc.Stack(
                                    [
                                        dmc.Text(
                                            week_day.day,
                                            c=(
                                                "dimmed"
                                                if week_day.month
                                                != datetime.now().month
                                                else "inerhit"
                                            ),
                                        )
                                    ],
                                    h="100%",
                                    w="100%",
                                ),
                                className="center-content-horizontal",
                                style={'align-content': 'flex-start'},
                                p=2
                            )
                            for week_day in week_days
                        ]
                    )
                    for week_days in cal.monthdatescalendar(
                        datetime.now().year, datetime.now().month
                    )
                ]
            ),
        ],
        # withRowBorders=False,
        # w="max-content",
        # mx="auto",
        mih="100%",
    )

    return maxi_calendar
