from datetime import datetime, timedelta
import plotly.express as px
from plotly.graph_objs import Figure
from pandas import DataFrame


def color_discrete_map_create(dataframe:DataFrame, pk:str, vk:str) -> dict:
    '''
        Return dict of color discrete map based on given dataframe
        pk - Primary Key
        vk - Value Key
    '''
    color_map = {}
    for i, row in dataframe.iterrows():
        if row[pk] not in color_map:
            color_map[row[pk]] = row[vk]

    print(color_map)
    return color_map


def pie_create(dataframe:DataFrame) -> Figure:
    '''
        Return plotly pie Figure of state causes
    '''

    pie = px.pie(
        data_frame=dataframe,
        names='reason',
        values='duration',
        height=320,
        hole=.2,
        color='reason',
        color_discrete_map=color_discrete_map_create(dataframe, 'reason', 'color')
    )
    return pie


def timeline_create(dataframe:DataFrame) -> Figure:
    '''
        Return plotly timeline Figure of state durations
    '''
    head = dataframe.head(1)
    shift_day = dataframe['Календарный день'].values[0]
    shift_begin_str = shift_day + ' ' + head['Начало смены'].values[0]
    shift_begin = datetime.strptime(shift_begin_str, '%Y-%m-%d %H:%M:%S') - timedelta(hours=1)
    shift_end = datetime.strptime(shift_begin_str, '%Y-%m-%d %H:%M:%S') + timedelta(hours=1, days=1)

    timeline = px.timeline(
        data_frame=dataframe,
        x_start='Начало состояния',
        x_end='Конец состояния',
        y='Название точки учета',
        height=300,
        color='Причина',
        color_discrete_map={'Вычисление': '#3d0a42', 'Заточка инструмента': '#eac117', 'Короткая остановка': '#e0827b', 'Наладка': '#4169e1', 'Обед 30мин': '#bcb88a', 'Обед 60мин': '#bcb88a', 'Перерыв 5мин': '#FF8C00', 'Подготовка к выполнению см/з': '#ff00ff', 'Поиск заготовок': '#e77474', 'Причина не указана': '#ed1c09', 'Работа': '#2ecc40', 'Слесарная операция': '#af9b84', 'См. задание выполнено': '#cd5c5c', 'Тех.обслуживание оборудования': '#4169e4'},
        hover_data={
            'Состояние':True,
            'Причина':True,
            'Название точки учета':False,
            'Цвет':False,
            'Начало состояния':True,
            'Конец состояния':False,
            'Сменный день':True,
            'Смена':True,
            'Оператор':True,
            'Длительность':True,
        }
    )
    timeline.update_layout(showlegend=False, yaxis={"title":''}, xaxis_range=[shift_begin, shift_end])
    return timeline