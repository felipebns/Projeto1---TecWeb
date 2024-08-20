from utils import load_data, load_template, build_response, alteraDB
import json
import urllib

def index(request):

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, details=dados.content, id=dados.id)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            chave_valor = chave_valor.split('=')
            params[chave_valor[0]] = chave_valor[1]

        notes = adiciona(params, note_template, notes)

        alteraDB(params=params)

        return build_response(code=303, reason='See Other', headers='Location: /')

    return build_response(body=load_template('index.html').format(notes=notes))

def adiciona(params, note_template, notes):
    params['titulo'] = urllib.parse.unquote_plus(params['titulo'], encoding='utf-8', errors='replace')
    params['detalhes'] = urllib.parse.unquote_plus(params['detalhes'], encoding='utf-8', errors='replace')

    notes_usuario = [
        note_template.format(title=params['titulo'], details=params['detalhes'])
    ]
    notes += '\n'.join(notes_usuario)

    return notes

