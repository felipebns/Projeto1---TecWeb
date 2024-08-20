from pathlib import Path
import json
import sqlite3
from database import Database
from database import Note

db = Database('notes')

def extract_route(requisicao):
    route = requisicao.split()[1]

    if route[0] == '/':
        route = route.replace('/', '', 1)
    
    return route

def read_file(path):
    return open(path, mode='rb').read()

def load_data():
    return db.get_all()

def load_template(template):
    path = f'Docs/templates/{template}'
    return open(path, mode='r+', encoding="utf-8").read()

def build_response(body='', code=200, reason='OK', headers=''):
    if headers:
        response = f"HTTP/1.1 {code} {reason}\n{headers}\n\n{body}".encode()

    else:
        response = f"HTTP/1.1 {code} {reason}\n\n{body}".encode()

    return response

def alteraDB(params):
    db.add(Note(title=params['titulo'], content=params['detalhes']))

def delete():
    pass