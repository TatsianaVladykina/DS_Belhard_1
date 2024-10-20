import pandas as pd
import pathlib as Path
import os
import json
import requests

def Load_data(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == '.csv':
        try:
            csv_file = pd.read_csv(file_path, encoding='ISO-8859-1')
        except UnicodeDecodeError:
            csv_file = pd.read_csv(file_path, encoding='utf-8', errors='ignore')
        return csv_file
    
    elif extension == '.json':
        with open(file_path, 'r', encoding='utf-8') as JSON:
            json_file = json.load(JSON)
        return json_file
    
    elif 'api' in file_path:
        api_file = requests.get(file_path)
        return api_file.text
    
    else:
        print('Неподдерживаемый формат файла')
        return None