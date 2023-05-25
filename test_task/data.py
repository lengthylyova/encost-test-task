import sqlite3
import pandas

# Подключение к БД
con = sqlite3.connect('./testDB.db')
# Изменение представления данных на выходе
con.row_factory = sqlite3.Row



# DataFrame всех данных из таблицы.
full_data = pandas.read_sql_query("SELECT * FROM 'sources';", con)


# Первая строка - для формирования общих данных (primary_data).
first_row = full_data.iloc[0]
primary_data = {
    'client_name':first_row['client_name'],
    'endpoint_id':first_row['endpoint_id'],
    'endpoint_name':first_row['endpoint_name'],
    'shift_day':first_row['shift_day'],
    'shift_begin':first_row['shift_begin'],
    'shift_end':first_row['shift_end'],
}


# DataFrame'ы для фигур отображаемых на странице.
# pie_df - для круговой диаграммы
# timeline - для диаграммы Ганта
pie_df = pandas.read_sql_query("SELECT reason, color FROM 'sources';", con)
timeline_df = pandas.DataFrame({
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


cur = con.cursor()
# Все существующие в таблице состояния.
states = cur.execute("SELECT DISTINCT state from sources;")
states = states.fetchall()
