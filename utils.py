from pathlib import Path
import json

def extract_route(requisicao):
    route = requisicao.split()[1]

    if route[0] == '/':
        route = route.replace('/', '', 1)
    
    return route

def read_file(path):
    return open(path, mode='r+b').read()

def load_data(json_name):
    current = f'data/{json_name}'

    json_arquive = read_file(current)

    return json.loads(json_arquive)

def load_template(template):
    path = f'templates/{template}'
    return open(path, mode='r+').read()