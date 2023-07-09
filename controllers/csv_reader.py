import csv
import os
from sqlite3 import IntegrityError
from models.allmodels import Result, Rodovia, Video, Controle
from database import db

def check_and_populate_control_table():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o caminho absoluto do diretório do script principal
    folder_name = "dados"  
    csv_folder_path = os.path.join(script_dir, "..", folder_name)  # Caminho absoluto para a pasta "dados"

    filenames = [os.path.splitext(filename)[0] for filename in os.listdir(csv_folder_path) if filename.endswith('.csv')]
    existing_files = Controle.select().where(Controle.file_name.in_(filenames)).execute()
    existing_filenames = {file.file_name for file in existing_files}

    for filename in filenames:
        if filename not in existing_filenames:
            try:
                Controle.create(file_name=filename)
                file_path = os.path.join(csv_folder_path, filename + '.csv')
                populate_tables(file_path)
                populate_rodovia_table()  
            except IntegrityError:
                continue

def populate_tables(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Verifica se o arquivo já existe na tabela controle
    file_name = os.path.basename(file_path)
    if Controle.select().where(Controle.file_name == file_name).exists():
        return

    name_min_km = {}
    name_max_km = {}
    rodovia_min_km = {}
    rodovia_max_km = {}

    for row in rows:
        name = row['name']
        rodovia = row['highway']
        km = float(row['km'])

        if name not in name_min_km or km < name_min_km[name]:
            name_min_km[name] = km
        if name not in name_max_km or km > name_max_km[name]:
            name_max_km[name] = km

        if rodovia not in rodovia_min_km or km < rodovia_min_km[rodovia]:
            rodovia_min_km[rodovia] = km
        if rodovia not in rodovia_max_km or km > rodovia_max_km[rodovia]:
            rodovia_max_km[rodovia] = km

    videos_batch = [{'name': name, 'km_ini': name_min_km[name], 'km_final': name_max_km[name]} for name in name_min_km]
    rodovias_batch = [{'rodovia': rodovia, 'km_ini': rodovia_min_km[rodovia], 'km_final': rodovia_max_km[rodovia]} for rodovia in rodovia_min_km]

    try:
        with db.atomic():
            batch_size = 100  # Define o tamanho do lote
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                Result.insert_many(batch).execute()
            
            Video.insert_many(videos_batch).execute()
    except IntegrityError as e:
        print(f"Erro ao inserir registros em 'Result': {e}")

def populate_rodovia_table():
    rodovias_dict = {}

    # Obter valores mínimo e máximo de 'km' para cada rodovia
    query = Result.select(Result.highway, Result.km).distinct().order_by(Result.highway, Result.km)
    for result in query:
        rodovia = result.highway
        km = result.km

        if rodovia not in rodovias_dict:
            rodovias_dict[rodovia] = {'km_ini': km, 'km_final': km}
        else:
            if km < rodovias_dict[rodovia]['km_ini']:
                rodovias_dict[rodovia]['km_ini'] = km
            if km > rodovias_dict[rodovia]['km_final']:
                rodovias_dict[rodovia]['km_final'] = km

    try:
        with db.atomic():
            for rodovia, data in rodovias_dict.items():
                existing_rodovia = Rodovia.get_or_none(rodovia=rodovia)
                if existing_rodovia:
                    existing_rodovia.km_ini = min(existing_rodovia.km_ini, data['km_ini'])
                    existing_rodovia.km_final = max(existing_rodovia.km_final, data['km_final'])
                    existing_rodovia.save()
                else:
                    Rodovia.create(rodovia=rodovia, km_ini=data['km_ini'], km_final=data['km_final'])
    except IntegrityError as e:
        print(f"Erro ao inserir registros em 'Rodovia': {e}")