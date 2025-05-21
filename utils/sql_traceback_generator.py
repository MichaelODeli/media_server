import traceback

import dash_mantine_components as dmc


def generate_sql_traceback(er, from_search=False):
    """

    :param er:
    :param from_search:
    :return:
    """
    err_cont = dmc.Alert(
        dmc.Stack(
            [
                dmc.Text(
                    "SQLite error: %s" % (" ".join(er.args)),
                    style={"margin-bottom": "0 !important"},
                ),
                dmc.Text(
                    f"Exception class is: {er.__class__}",
                    style={"margin": "5px !important"},
                ),
                dmc.Space(h=10),
                dmc.Text("SQLite traceback:", style={"margin": "5px !important"}),
            ]
            + [
                dmc.Text(f"{line}", style={"margin": "5px !important"})
                for line in traceback.format_exception(er)
            ],
            gap=0,
            justify="center",
        ),
        w="70%" if not from_search else '100%',
        title="SQL Error",
        color="red",
        radius="md",
        className="alert-pos" if not from_search else None,
    )
    return err_cont
