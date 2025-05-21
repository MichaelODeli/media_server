import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html, register_page
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

register_page(
    __name__,
    path="/login",
)


def layout(**kwargs):
    """

    :param kwargs:
    :return:
    """
    return (
        dmc.Stack(
            align="center",
            pt=50,
            w=300,
            m="auto",
            gap="md",
            children=[
                html.H4("Авторизация"),
                dcc.Location(id="url_login", refresh=True),
                dmc.TextInput(
                    label="Имя пользователя",  # потом будет табельный номер
                    placeholder="Ваше имя пользователя",
                    leftSection=DashIconify(icon="radix-icons:person"),
                    id="uname-box",
                    w="100%",
                ),
                dmc.SegmentedControl(
                    id="passwd-type",
                    value="pin",
                    data=[
                        {"value": "pin", "label": "Вход по пинкоду"},
                        {"value": "passwd", "label": "Вход по паролю"},
                    ],
                    fullWidth=True,
                    w='100%'
                ),
                dmc.Box(id="passwd-field", w='100%'),
                dmc.Checkbox(label="Запомнить меня", checked=True, id="login-remember"),
                dmc.Button(
                    "Войти",
                    id="login-button",
                    variant="outline",
                    fullWidth=True,
                    n_clicks=0,
                ),
            ],
        ),
    )


@callback(Output("passwd-field", "children"), Input("passwd-type", "value"))
def format_passwd_field(value):
    """

    :param value:
    :return:
    """
    if value == "pin":
        return dmc.PinInput(
            w="100%",
            id="pwd-box",
            length=5,
            type="number",
            className='justify-content-center',
            mask=True
        )
    elif value == "passwd":
        return dmc.PasswordInput(
            placeholder="Ваш пароль",
            leftSection=DashIconify(icon="radix-icons:lock-closed"),
            id="pwd-box",
            w="100%",
        )
    else:
        raise PreventUpdate
