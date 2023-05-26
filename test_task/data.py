import sqlite3
import pandas

'''Подключение к БД'''
con = sqlite3.connect('./testDB.db')

'''Изменение представления данных на выходе'''
con.row_factory = sqlite3.Row


# DataFrame всех данных из таблицы.
def full_df(con=con) -> pandas.DataFrame:
    '''
        Return DataFrame of all data from db.
    '''
    query = "SELECT * FROM 'sources';"
    full_data = pandas.read_sql_query(query, con)

    return full_data


def pie_df(con=con) -> pandas.DataFrame:
    '''
        Return DataFrame of data from db for pie figure
    '''
    query = "SELECT reason, color FROM 'sources';"
    pie_data = pandas.read_sql_query(query, con)

    return pie_data


def timeline_df(con=con) -> pandas.DataFrame:
    '''
        Return DataFrame of data from db for timeline figure.
    '''
    full_data = full_df(con)
    timeline_data = pandas.DataFrame({
        'Имя клиента':full_data['client_name'],
        'Название точки учета':full_data['endpoint_name'],
        'Состояние':full_data['state'],
        'Причина':full_data['reason'],
        'Начало':full_data['state_begin'],
        'Конец':full_data['state_end'],
        'Длительность':full_data['duration_min'],
        'Сменный день':full_data['shift_day'],
        'Смена':full_data['shift_name'],
        'Оператор':full_data['operator'],
        'Цвет':full_data['color'],
    })

    return timeline_data


def states_fetchall():
    '''
        Return all states from 'state' column of db.
    '''
    cur = con.cursor()
    query = "SELECT DISTINCT state from sources;"
    states = cur.execute(query)
    states = states.fetchall()

    return states
