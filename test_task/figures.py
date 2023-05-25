import plotly.express as px
from data import pie_df, timeline_df



# Круговая диаграмма причин состояний
pie = px.pie(data_frame=pie_df,
             names='reason',
             height=320,
             hole=.2,
             color='color'
            )


# Диаграмма Ганта длительностей причин состояний
timeline = px.timeline(
    data_frame=timeline_df,
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