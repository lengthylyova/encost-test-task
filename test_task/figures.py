import plotly.express as px
from plotly.graph_objs import Figure
from pandas import DataFrame



def pie_create(dataframe:DataFrame) -> Figure:
    '''
        Return plotly pie Figure of state causes
    '''
    pie = px.pie(
        data_frame=dataframe,
        names='reason',
        height=320,
        hole=.2,
        color='color'
    )
    return pie


def timeline_create(dataframe:DataFrame) -> Figure:
    '''
        Return plotly timeline Figure of state durations
    '''
    timeline = px.timeline(
        data_frame=dataframe,
        x_start='Начало',
        x_end='Конец',
        y='Название точки учета',
        height=300,
        color='Цвет',    
        hover_data={
            'Состояние':True,
            'Причина':True,
            'Название точки учета':False,
            'Цвет':False,
            'Начало':True,
            'Конец':False,
            'Сменный день':True,
            'Смена':True,
            'Оператор':True,
            'Длительность':True,
        }
    )
    timeline = timeline.update_layout(showlegend=False, yaxis={"title":''})
    return timeline