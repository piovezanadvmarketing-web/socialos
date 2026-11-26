#!/usr/bin/env python3
"""Fila de postagem do SocialOS, para a esteira (Nuru publica o que está Aprovado).

  python3 fila.py fila [--todos]          posts com Publicação = Aprovado (ou todos), em JSON, por data e hora
  python3 fila.py marcar <id> publicado <link>
  python3 fila.py marcar <id> falhou "<motivo>"

Lê url.txt e senha.txt desta pasta. Grava só o post marcado: relê o estado, troca as propriedades dele e
grava com a revisão de agora; se outra pessoa salvou no meio, tenta de novo (até 5 vezes).
"""
import json, sys, time, urllib.request, urllib.parse, pathlib
AQUI = pathlib.Path(__file__).resolve().parent
URL = (AQUI / 'url.txt').read_text().strip(); CHAVE = (AQUI / 'senha.txt').read_text().strip()
PUB, DRIVE, LINK, MOTIVO = 'p-publicacao', 'p-drive', 'p-link', 'p-falha'
VALORES = {'rascunho', 'aprovado', 'publicado', 'falhou'}

def ler():
    with urllib.request.urlopen(URL + '?' + urllib.parse.urlencode({'chave': CHAVE}), timeout=60) as r:
        d = json.load(r)
    if d.get('erro'): sys.exit('erro do servidor: ' + d['erro'])
    return d

def gravar(base, state):
    corpo = json.dumps({'chave': CHAVE, 'base': base, 'state': state}).encode()
    req = urllib.request.Request(URL, data=corpo, headers={'Content-Type': 'text/plain;charset=utf-8'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def fila(todos=False):
    d = ler(); s = d['state']; redes = s.get('networks', {})
    out = []
    for p in s['posts']:
        st = (p.get('props') or {}).get(PUB) or 'rascunho'
        if not todos and st != 'aprovado': continue
        out.append({
            'id': p['id'], 'titulo': p.get('title', ''), 'data': p.get('date', ''), 'hora': p.get('time', ''),
            'redes_id': p.get('networks') or [p.get('network')],
            'redes': [redes.get(n, {}).get('name', n) for n in (p.get('networks') or [p.get('network')])],
            'formatos': p.get('formats') or [p.get('format')],
            'legenda': p.get('caption', ''), 'hashtags': p.get('hashtags', ''),
            'arquivo_drive': (p.get('props') or {}).get(DRIVE, ''), 'publicacao': st,
            'link_publicado': (p.get('props') or {}).get(LINK, ''),
        })
    out.sort(key=lambda x: (x['data'] or '9999', x['hora'] or '99'))
    print(json.dumps({'revisao': d['rev'], 'posts': out}, ensure_ascii=False, indent=2))

def marcar(pid, valor, extra):
    if valor not in VALORES: sys.exit('valor deve ser um de ' + ', '.join(sorted(VALORES)))
    for _ in range(5):
        d = ler(); s = d['state']
        p = next((x for x in s['posts'] if x['id'] == pid), None)
        if not p: sys.exit('post não achado: ' + pid)
        p.setdefault('props', {})[PUB] = valor
        if valor == 'publicado' and extra: p['props'][LINK] = extra
        if valor == 'falhou' and extra: p['props'][MOTIVO] = extra
        p['updatedAt'] = int(time.time() * 1000)
        r = gravar(d['rev'], s)
        if not r.get('conflito') and not r.get('erro'):
            print(json.dumps({'ok': True, 'id': pid, 'publicacao': valor, 'revisao': r.get('rev')}, ensure_ascii=False)); return
        time.sleep(1.5)
    sys.exit('não consegui gravar depois de 5 tentativas')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'fila': fila('--todos' in a)
    elif a[0] == 'marcar' and len(a) >= 3: marcar(a[1], a[2], a[3] if len(a) > 3 else '')
    else: print(__doc__)
