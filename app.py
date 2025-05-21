import os

import dash
import dash_mantine_components as dmc
import flask
from dash import dcc, html
from dash_extensions.pages import setup_page_components
from dotenv import dotenv_values

from callbacks import call_app
from variables import styles


config = {
    **dotenv_values(".env"),  # load variables
    # **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

# flask and dash configuration
server = flask.Flask(__name__)
app = dash.Dash(
    # name=config["APP_NAME"],
    __name__,
    server=server,
    use_pages=True,
    external_stylesheets=styles.STYLESHEETS,
    title=config["WEB_PAGE_TITLE"],
    update_title=config["WEB_PAGE_LOADING_TITLE"],
    suppress_callback_exceptions=True,
    pages_folder=os.path.abspath("pages")
)
# app = dash.Dash(
#     __name__,
#     server=server,
#     use_pages=True,
#     external_stylesheets=styles.STYLESHEETS,
#     suppress_callback_exceptions=True,
#     pages_folder=os.path.abspath("pages")
# )


# Конструкция всего макета
app.layout = dmc.MantineProvider(
    children=[
        dmc.AppShell(
            [
                dmc.AppShellHeader(
                    children="",
                    id="navbar-children",
                    px=25,
                    py=10,
                    w="100dvw",
                    zIndex=100,
                ),
                dmc.AppShellMain(
                    [
                        dash.page_container,
                        dmc.LoadingOverlay(
                            visible=True,
                            id="loading-overlay",
                            zIndex=1000,
                            overlayProps={"radius": "sm", "blur": 5},
                            loaderProps={"size": "lg"},
                        ),
                    ],
                    id="server-blocker",
                ),
            ],
            header={"height": 60},
            id="appshell-props",
        ),
        dmc.NotificationProvider(position="bottom-right"),
        setup_page_components(),
        html.Div(id="notifications-container-search"),
        dcc.Store(id="server-avaliablity"),
        dcc.Location(id="url-audio"),
        dcc.Location(id="url"),
        html.Div(id="dummy-1"),
    ],
    id="mantine_theme",
    # defaultColorScheme="light",
    theme={
        "primaryColor": styles.PRIMARY_COLOR,
        "fontFamily": styles.FONT_FAMILY,
        "headings": styles.HEADINGS,
        "colors": styles.COLORS,
    },
)


call_app.get_server_blocker_callback(app)
call_app.get_navbar_callbacks(app)
call_app.get_navbar_search_bar_callbacks(app)


dev = bool(config["APP_DEBUG_ENABLED"])

if __name__ == "__main__":
    if dev:
        app.run(
            debug=True,
            host=config["APP_HOST"],
            port=int(config["APP_PORT"])
        )
    else:
        from waitress import serve
        serve(app.server, host=config["APP_HOST"],
              port=int(config["APP_PORT"]))
