from utils import load_data, load_template, build_response
import json
import urllib

def index(request):

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'])
        for dados in load_data('notes.json')
    ]
    notes = '\n'.join(notes_li)
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            # AQUI É COM VOCÊ
            chave_valor = chave_valor.split('=')
            params[chave_valor[0]] = chave_valor[1]
        params['titulo'] = urllib.parse.unquote_plus(params['titulo'], encoding='utf-8', errors='replace')
        params['detalhes'] = urllib.parse.unquote_plus(params['detalhes'], encoding='utf-8', errors='replace')

        # Cria uma lista de <li>'s para cada anotação
        # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions

        notes = adiciona(params, note_template, notes)

        with open('data/notes.json', 'r+') as f:
            data = json.load(f)
            data.append(params) 
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()     # remove remaining part

        return build_response(code=303, reason='See Other', headers='Location: /')

    return build_response(body=load_template('index.html').format(notes=notes))

def adiciona(params, note_template, notes):
    notes_usuario = [
        note_template.format(title=params['titulo'], details=params['detalhes'])
    ]
    notes += '\n'.join(notes_usuario)

    return urllib.parse.unquote_plus(notes, encoding='utf-8', errors='replace')
