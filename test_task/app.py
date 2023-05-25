from dash import html, Output, Input, State, dcc
from dash_extensions.enrich import DashProxy, ServersideOutputTransform, MultiplexerTransform
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from data import primary_data, states, timeline_df
from figures import pie, timeline



multiselect = [{"value":states[i]['state'], "label":states[i]['state']} for i in range(len(states))]

CARD_STYLE = dict(withBorder=True, shadow="sm", radius="md",)

class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(), MultiplexerTransform()], **kwargs)

app = EncostDash(name=__name__)

def get_layout():
    return html.Div([
        dmc.Paper([
            dmc.Grid([
                dmc.Col([
                    dmc.Card([
                        dmc.Text(f"Клиент: {primary_data['client_name']}", weight=700, size=25),
                        dmc.Text(f"Сменный день: {primary_data['shift_day']}", weight=700, size=16),
                        dmc.Text(f"Точка учета: {primary_data['endpoint_name']} (id: {primary_data['endpoint_id']})", weight=700, size=16),
                        dmc.Text(f"Начало периода: {primary_data['shift_begin']}", weight=700, size=16),
                        dmc.Text(f"Конец периода: {primary_data['shift_end']}", weight=700, size=16, style={"margin-bottom":10}),
                        
                        dmc.MultiSelect(
                            placeholder="",
                            id="multi-select",
                            value=[],
                            data=multiselect,
                            style={"width": "50%", "marginBottom": 10},),
                        dmc.Button(
                            'Фильтровать',
                            id='button1'),
                        html.Div('', id='output')],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(
                            id='diagram',
                            figure=pie,
                        )],
                        **CARD_STYLE),
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(
                            id='timeline',
                            figure=timeline
                        )],
                        **CARD_STYLE)
                ], span=12),
            ], gutter="xl")
        ])
    ])


app.layout = get_layout()

# @app.callback(Output('timeline', 'figure'), State('multi-select', 'value'), Input('button1', 'n_clicks'), prevent_initial_call=True,)
# def update_timeline(value, click):
#     return new_timeline


if __name__ == '__main__':
    app.run_server(debug=True)
