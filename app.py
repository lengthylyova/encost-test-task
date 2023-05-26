import os
import sqlite3
from dash import Output, State, Input
from dash_extensions.enrich import DashProxy, ServersideOutputTransform, MultiplexerTransform
from dash.exceptions import PreventUpdate
from server.layout import get_layout
from server.data import db_connect, timeline_df
from server.figures import timeline_create



class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(), MultiplexerTransform()], **kwargs)



app = EncostDash(name=__name__)
app.layout = get_layout()


@app.callback(Output('timeline', 'figure'), State('multi-select', 'value'), Input('button1', 'n_clicks'), prevent_initial_call=True,)
def update_timeline(value, click):
    if click is None:
        return PreventUpdate
    
    con = db_connect()

    if value == []:
        timeline = timeline_create(timeline_df(con))
        return timeline
    
    df = timeline_df(con)
    df = df[df['Состояние'].isin(value)]
    timeline = timeline_create(df)

    return timeline


if __name__ == '__main__':
    app.run_server(debug=True)
