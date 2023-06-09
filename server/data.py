from datetime import datetime
import os
import sqlite3
import pandas


''''''
DIR_PATH = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1])



def db_connect() -> sqlite3.Connection:
    '''
        Return connection to db.
    '''
    con = sqlite3.connect(f'{DIR_PATH}\\testDB.db')
    con.row_factory = sqlite3.Row
    
    return con


def full_df(con:sqlite3.Connection) -> pandas.DataFrame:
    '''
        Return DataFrame of all data from db.
    '''
    query = "SELECT * FROM 'sources';"
    full_data = pandas.read_sql_query(query, con)
    return full_data


def pie_df(con:sqlite3.Connection) -> pandas.DataFrame:
    '''
        Return DataFrame of data from db for pie figure
    '''
    query = "SELECT reason, color, SUM(duration_min) as duration FROM 'sources' GROUP BY reason;"
    pie_data = pandas.read_sql_query(query, con)
    return pie_data


def timeline_df(con:sqlite3.Connection) -> pandas.DataFrame:
    '''
        Return DataFrame of data from db for timeline figure.
    '''
    full_data = full_df(con)
    timeline_data = pandas.DataFrame({
        'Имя клиента':full_data['client_name'],
        'Название точки учета':full_data['endpoint_name'],
        'Состояние':full_data['state'],
        'Причина':full_data['reason'],
        'Начало состояния':full_data['state_begin'],
        'Конец состояния':full_data['state_end'],
        'Длительность':full_data['duration_min'],
        'Сменный день':full_data['shift_day'],
        'Смена':full_data['shift_name'],
        'Оператор':full_data['operator'],
        'Цвет':full_data['color'],
        'Начало смены':full_data['shift_begin'],
        'Конец смены':full_data['shift_end'],
        'Календарный день':full_data['calendar_day'],
    })

    return timeline_data


def reasons_fetchall(con:sqlite3.Connection) -> list:
    '''
        Return all reasons from 'state' column of db.
    '''
    cur = con.cursor()
    query = "SELECT DISTINCT reason from sources;"
    reasons = cur.execute(query)
    reasons = reasons.fetchall()

    return reasons
