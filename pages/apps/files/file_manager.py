# tree view from https://dash-blueprint-components.com/core/components/tree

# from dash import (
#     dcc,
#     html,
#     Input,
#     Output,
#     callback,
#     register_page,
#     State,
#     Input,
#     Output,
#     no_update,
# )
# import dash_mantine_components as dmc
# import dash_bootstrap_components as dbc
# from flask import request
# from datetime import datetime
# from dash_iconify import DashIconify
# from controllers import cont_files as cont_f
# from controllers import service_controller as service

# register_page(__name__, path="/files", icon="fa-solid:home")


# def layout(l="n", **kwargs):
#     # lazy load block
#     if l == "n":
#         return dmc.Container()
#     else:
#         service.logPrinter(request.remote_addr, 'files', 'page opened')
#         return dmc.Container(
#             children=[
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             [
#                                 dmc.Stack(
#                                     [
#                                         dmc.Title("Дерево папок", order=4),
#                                         cont_f.treeContent(source="col")
#                                     ],
#                                     className="block-background",
#                                 )
#                             ],
#                             className="hided_column",
#                             width=3,
#                         ),
#                         dbc.Col(
#                             [
#                                 cont_f.blockFilesList(),
#                             ]
#                         ),
#                     ]
#                 ),
#                 dmc.Affix(
#                     dmc.ActionIcon(
#                         DashIconify(
#                             icon="iconamoon:menu-burger-horizontal",
#                             width=35,
#                             color="var(--bs-primary)",
#                         ),
#                         size="50px",
#                         radius="xl",
#                         variant="default",
#                         id="open-drawer",
#                     ),
#                     position={"bottom": 20, "left": 20},
#                     className="shown-affix",
#                 ),
#                 cont_f.getDrawer(),
#             ],
#             pt=20,
#             className="dmc-container adaptive-container",
#         )


# @callback(
#     Output("drawer-tree", "opened"),
#     Input("open-drawer", "n_clicks"),
#     prevent_initial_call=True,
# )
# def drawerWithTree(n_clicks):
#     return True
