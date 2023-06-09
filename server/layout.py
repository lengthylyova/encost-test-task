from dash import html, dcc
import dash_mantine_components as dmc
from server.data import db_connect, reasons_fetchall, pie_df, timeline_df, full_df
from server.figures import pie_create, timeline_create


CARD_STYLE = dict(withBorder=True, shadow="sm", radius="md", style={"height":"46vh", "overflow":"none", "z-index":"99"})


def get_layout() -> html:
    '''
        Return html layout for app.
    '''
    con = db_connect()

    full_data = full_df(con)

    first_row = full_data.iloc[0]
    primary_data = {
        'client_name':first_row['client_name'],
        'endpoint_id':first_row['endpoint_id'],
        'endpoint_name':first_row['endpoint_name'],
        'shift_day':first_row['shift_day'],
        'shift_begin':first_row['shift_begin'],
        'shift_end':first_row['shift_end'],
    }

    timeline = timeline_create(timeline_df(con))
    pie = pie_create(pie_df(con))

    reasons = reasons_fetchall(con)
    multiselect = [
        {"value":reasons[i]['reason'],
         "label":reasons[i]['reason']} for i in range(len(reasons))]

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
                            style={"width": "50%", "marginBottom": 10, "z-index":"101"},),
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