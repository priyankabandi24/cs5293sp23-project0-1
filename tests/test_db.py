from project0 import main
import sqlite3
def test_insert_info_to_db():
    info = [{'date_time': '01/01/2022 01:30', 'incident_number': '2022-00001234', 'nature': 'TRAFFIC STOP', 'location': '123 MAIN ST', 'origin': 'JONES'},
            {'date_time': '01/02/2022 08:15', 'incident_number': '2022-00001235', 'nature': 'ASSAULT', 'location': '456 ELM ST', 'origin': 'SMITH'},
            {'date_time': '01/02/2022 12:00', 'incident_number': '2022-00001236', 'nature': 'TRAFFIC ACCIDENT', 'location': '789 OAK ST', 'origin': 'WILLIAMS'}]
    main.insert_info_to_db(info)
    conn = sqlite3.connect('incidents.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nature, COUNT() FROM incidents GROUP BY nature ORDER BY COUNT() DESC')
    results = cursor.fetchall()
    assert results == [('TRAFFIC STOP', 1), ('TRAFFIC ACCIDENT', 1), ('ASSAULT', 1)]
