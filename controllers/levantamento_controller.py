import csv
from peewee import fn
from models.allmodels import View,Result
from peewee import SqliteDatabase
from database import db


View.create_table()

#Permitir consulta do tipo qual Km possui maior incidência de determinado item 
def get_highest_incidence_km(item):
    try:
        query = (
            Result
            .select()
            .where(Result.item == item)
            .group_by(Result.km)
            .order_by(fn.COUNT(Result.item).desc())
            .limit(1)
        )
        highest_km = query[0].km if query else None
        return highest_km
    except Exception as e:
        print(f"Erro ao obter o quilômetro com maior incidência do item '{item}': {e}")
        return None

#Agrupamento dos dados e exportação
def export_results_to_csv(highway):
    cursor = db.execute_sql(f'''
        SELECT highway, km,
            SUM(CASE WHEN item = 'Buraco' THEN 1 ELSE 0 END) AS buraco,
            SUM(CASE WHEN item = 'Remendo' THEN 1 ELSE 0 END) AS remendo,
            SUM(CASE WHEN item = 'Trinca' THEN 1 ELSE 0 END) AS trinca,
            SUM(CASE WHEN item = 'Placa' THEN 1 ELSE 0 END) AS placa,
            SUM(CASE WHEN item = 'Drenagem' THEN 1 ELSE 0 END) AS drenagem
        FROM results
        WHERE highway = ?
        GROUP BY highway, km
        ORDER BY highway, km
    ''', params=(highway,))

    file_name = f"rodovia_{highway}.csv"
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['highway', 'km', 'buraco', 'remendo', 'trinca', 'placa', 'drenagem'])
        writer.writeheader()

        for row in cursor.fetchall():
            writer.writerow({
                'highway': row[0],
                'km': row[1],
                'buraco': row[2],
                'remendo': row[3],
                'trinca': row[4],
                'placa': row[5],
                'drenagem': row[6]
            })

    return True