from dash import html, register_page
import dash_mantine_components as dmc

register_page(
    __name__,
    path="/logout",
)

layout = dmc.Stack(
    [
        html.H5("Вы успешно вышли из своего аккаунта."),
        dmc.Anchor('На главную', href='/', underline='always')
    ],
    style={"margin-top": "70px"},
    align='center'
)
