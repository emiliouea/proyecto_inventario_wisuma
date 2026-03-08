import os
import json
import csv

def save_data_to_txt(data, filename, delimiter='|'):
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        for item in data:
            # Assuming item is a dictionary and values are strings or can be converted to strings
            line = delimiter.join(str(value) for value in item.values())
            f.write(line + "\n")
    return True, f"Datos guardados en {filename} exitosamente."

def load_data_from_txt(filename, delimiter='|', keys=None):
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    data = []
    if not os.path.exists(filepath):
        return [], f"El archivo {filename} no existe."
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            values = line.strip().split(delimiter)
            if keys and len(values) == len(keys):
                item = dict(zip(keys, values))
                data.append(item)
            else:
                # If keys are not provided or don't match, return as a list of values
                data.append(values)
    return data, f"Datos cargados desde {filename} exitosamente."

def save_data_to_json(data, filename):
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return True, f"Datos guardados en {filename} exitosamente."

def load_data_from_json(filename):
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    if not os.path.exists(filepath):
        return [], f"El archivo {filename} no existe."
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data, f"Datos cargados desde {filename} exitosamente."

def save_data_to_csv(data, filename, fieldnames):
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(filepath, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return True, f"Datos guardados en {filename} exitosamente."

def load_data_from_csv(filename):
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    data = []
    if not os.path.exists(filepath):
        return [], f"El archivo {filename} no existe."
    with open(filepath, "r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data, f"Datos cargados desde {filename} exitosamente."
