from dash_extensions.enrich import DashProxy, ServersideOutputTransform, MultiplexerTransform
# from dash.exceptions import PreventUpdate
from layout import get_layout



class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(), MultiplexerTransform()], **kwargs)



app = EncostDash(name=__name__)
app.layout = get_layout()


# @app.callback(Output('timeline', 'figure'), State('multi-select', 'value'), Input('button1', 'n_clicks'), prevent_initial_call=True,)
# def update_timeline(value, click):
#     return new_timeline


if __name__ == '__main__':
    app.run_server(debug=True)
