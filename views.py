from utils import load_data, load_template, build_response, add, get_element, update_element, get_popup, update_popup, get_titulos
import urllib

def index(request):

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, details=dados.content, id=dados.id)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)
    popup_str = get_popup()

    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            chave_valor = chave_valor.split('=')
            params[chave_valor[0]] = chave_valor[1]
    
        params['titulo'] = urllib.parse.unquote_plus(params['titulo'], encoding='utf-8', errors='replace')
        params['detalhes'] = urllib.parse.unquote_plus(params['detalhes'], encoding='utf-8', errors='replace')

        for k,v in params.items():
            titulos = get_titulos()
            if v == "":
                update_popup("Título e/ou conteúdo vazios!")
                return build_response(code=303, reason='See Other', headers='Location: /')
            if v in titulos:
                update_popup("Título repetido!")
                return build_response(code=303, reason='See Other', headers='Location: /')
            
        update_popup("")
        add(params=params)

        return build_response(code=303, reason='See Other', headers='Location: /')

    return build_response(body=load_template('index.html').format(notes=notes, popup=popup_str))

def edit(request, id):
    
    edicao_template = load_template('edicao.html')
    elemento = get_element(id)

    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            chave_valor = chave_valor.split('=')
            params[chave_valor[0]] = chave_valor[1]

        params['titulo'] = urllib.parse.unquote_plus(params['titulo'], encoding='utf-8', errors='replace')
        params['detalhes'] = urllib.parse.unquote_plus(params['detalhes'], encoding='utf-8', errors='replace')
        params['id'] = int(id)
        if params['action'] == "salvar":
            update_element(params=params)   
            
        return build_response(code=303, reason='See Other', headers='Location: /')

    return build_response(body=edicao_template.format(title=elemento.title, details=elemento.content))
