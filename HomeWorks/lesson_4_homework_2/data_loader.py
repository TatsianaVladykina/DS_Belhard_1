import pandas as pd
import pathlib as Path
import os
import json
import requests

def Load_data(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == '.csv':
        csv_file = pd.read_csv(file_path)
        return csv_file
    elif extension == '.json':
        with open(file_path, 'r') as JSON:
            json_file = json.load(JSON)
        return json_file
    elif file_path.find('api') != -1:
        api_file = requests.get(file_path)
        return api_file.text
    else:
        return print('Неподдерживаемый формат файла')