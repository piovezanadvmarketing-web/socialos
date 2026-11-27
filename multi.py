# Gera base.html a partir de original.html: o post passa a ter várias redes (p.networks) e vários formatos (p.formats).
# p.network e p.format continuam como o primeiro de cada lista, para a cor, o limite de caracteres e o que já existia.
s = open('original.html', encoding='utf-8').read()
# Tema do Kivuli (26/11/2026): o <style> inteiro vem de tema.css.
i = s.index('<style>') + len('<style>'); j = s.index('</style>', i)
s = s[:i] + '\n' + open('tema.css', encoding='utf-8').read() + '\n' + s[j:]
def t(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

# migração
t("    if (!x.format) x.format = NETWORKS[x.network].formats[0];\n",
  "    if (!x.format) x.format = NETWORKS[x.network].formats[0];\n"
  "    x.networks = (Array.isArray(x.networks) ? x.networks : [x.network]).filter(n => NETWORKS[n]); if (!x.networks.length) x.networks = [x.network]; x.network = x.networks[0];\n"
  "    x.formats = (Array.isArray(x.formats) ? x.formats : [x.format]).filter(Boolean); if (!x.formats.length) x.formats = [x.format]; x.format = x.formats[0];\n")
# ajudantes, antes do filtro
t("const filtered = list => (ui.net === 'all' ? list : list.filter(p => p.network === ui.net));",
  "const nets = p => (p.networks && p.networks.length ? p.networks : [p.network]).filter(n => NETWORKS[n]);\n"
  "const fmts = p => (p.formats && p.formats.length ? p.formats : [p.format]).filter(Boolean);\n"
  "const fmtText = p => fmts(p).join(' + ');\n"
  "const netBadges = p => nets(p).map(netBadge).join('');\n"
  "const netPills = p => nets(p).map(netPill).join(' ');\n"
  "const netNames = p => nets(p).map(n => NETWORKS[n].name).join(' + ');\n"
  "const formatsOf = p => [...new Set([...nets(p).flatMap(n => NETWORKS[n].formats), ...fmts(p)])];\n"
  "const syncPost = p => { p.networks = nets(p); if (!p.networks.length) p.networks = [Object.keys(NETWORKS)[0]]; p.network = p.networks[0]; p.formats = fmts(p); if (!p.formats.length) p.formats = [NETWORKS[p.network].formats[0]]; p.format = p.formats[0]; };\n"
  "const filtered = list => (ui.net === 'all' ? list : list.filter(p => nets(p).includes(ui.net)));")
# seletor de rede: várias
t("title: 'Rede social', list: () => Object.entries(NETWORKS).map(([id, n]) => ({ id, name: n.name, color: n.color })), isSel: id => p.network === id,",
  "title: 'Rede social', multi: true, list: () => Object.entries(NETWORKS).map(([id, n]) => ({ id, name: n.name, color: n.color })), isSel: id => nets(p).includes(id),")
t("    onSelect: id => { if (p.network !== id) { p.network = id; const fm = NETWORKS[id].formats; if (!fm.includes(p.format)) p.format = fm[0]; touch(p); } },",
  "    onSelect: id => { const l = nets(p); if (l.includes(id)) { if (l.length > 1) p.networks = l.filter(n => n !== id); } else p.networks = [...l, id]; syncPost(p); touch(p); },")
# seletor de formato, novo
t("function pickTags(anchor, p) {",
  "function pickFormats(anchor, p) {\n"
  "  optionPicker(anchor, {\n"
  "    title: 'Formato', multi: true, list: () => FORMATOS.map(f => ({ id: f, name: f, color: '#94a3b8' })), isSel: id => fmts(p).includes(id),\n"
  "    onSelect: id => { const l = fmts(p); if (l.includes(id)) { if (l.length > 1) p.formats = l.filter(f => f !== id); } else p.formats = [...l, id]; syncPost(p); touch(p); },\n"
  "    onEdit: () => {},\n"
  "  });\n"
  "}\n"
  "function pickTags(anchor, p) {")
# apagar rede
t("const n = state.posts.filter(p => p.network === id).length;", "const n = state.posts.filter(p => nets(p).includes(id)).length;")
t("state.posts.forEach(p => { if (p.network === id) { p.network = fb; if (!NETWORKS[fb].formats.includes(p.format)) p.format = NETWORKS[fb].formats[0]; } });",
  "state.posts.forEach(p => { if (nets(p).includes(id)) { p.networks = nets(p).filter(n => n !== id); if (!p.networks.length) p.networks = [fb]; syncPost(p); } });")
# exibição
t("<div class=\"pmeta\">${netBadge(p.network)}<span>${esc(p.format)}</span>", "<div class=\"pmeta\">${netBadges(p)}<span>${esc(fmtText(p))}</span>")
t("<div class=\"card-meta\">${netBadge(p.network)}<span class=\"tag\">${esc(p.format)}</span>", "<div class=\"card-meta\">${netBadges(p)}<span class=\"tag\">${esc(fmtText(p))}</span>")
t("posts.filter(p => p.network === k).length", "posts.filter(p => nets(p).includes(k)).length", 2)
t("items: posts.filter(p => p.network === k) }", "items: posts.filter(p => nets(p).includes(k)) }")
t("title=\"${esc(N.name + ' · ' + p.format + ' · ", "title=\"${esc(netNames(p) + ' · ' + fmtText(p) + ' · ")
t("${p.title} ${p.caption} ${p.hashtags} ${p.format} ", "${p.title} ${p.caption} ${p.hashtags} ${fmtText(p)} ${netNames(p)} ")
t("format: (a, b) => a.format.localeCompare(b.format),", "format: (a, b) => fmtText(a).localeCompare(fmtText(b)),")
t("title=\"Trocar ou editar rede\">${netPill(p.network)}</button>", "title=\"Escolher uma ou mais redes\">${netPills(p)}</button>")
t("case 'format': return `<div class=\"lc\"><select class=\"cell\" data-lf=\"format\" data-id=\"${p.id}\">${opts([...new Set([...N.formats, p.format])].map(f => [f, f]), p.format)}</select></div>`;",
  "case 'format': return `<div class=\"lc\"><button class=\"cellbtn\" data-act=\"pick-format\" data-post=\"${p.id}\" title=\"Escolher um ou mais formatos\">${esc(fmtText(p))}</button></div>`;")
t("<span class=\"crumb\">${netBadge(p.network)} ${N.name} · ${esc(p.format)}</span>", "<span class=\"crumb\">${netBadges(p)} ${esc(netNames(p))} · ${esc(fmtText(p))}</span>")
t("title=\"Trocar, criar ou editar redes\">${netPill(p.network)}</button>", "title=\"Escolher uma ou mais redes\">${netPills(p)}</button>")
i = s.index('<div class="prop"><span class="prop-l">${icon(\'layers\', 14)} Formato</span><div class="prop-v"><select data-f="format">')
j = s.index('</select>', i) + len('</select>')
s = s[:i] + '<div class="prop"><span class="prop-l">${icon(\'layers\', 14)} Formato</span><div class="prop-v"><button class="pillbtn" data-act="pick-format" title="Escolher um ou mais formatos">${esc(fmtText(p))}</button>' + s[j:]
t("  const lim = NETWORKS[p.network].limit;", "  const lim = Math.min(...nets(p).map(n => NETWORKS[n].limit));")
t("  'pick-tags': el => {", "  'pick-format': el => { const p = getPost(el.dataset.post || ui.postId); if (p) pickFormats(el, p); },\n  'pick-tags': el => {")

# Formatos: só os quatro que a equipe usa (pedido do Samuel, 26/11/2026). Os de antes passam ao mais próximo.
t("  NETWORKS = s.networks;\n", "  for (const n of Object.values(s.networks)) n.formats = [...FORMATOS];\n  NETWORKS = s.networks;\n")
t("    x.formats = (Array.isArray(x.formats) ? x.formats : [x.format]).filter(Boolean);",
  "    x.formats = [...new Set((Array.isArray(x.formats) ? x.formats : [x.format]).filter(Boolean).map(paraFormato))];")
t("// NETWORKS aponta para state.networks (editável); migrate() reatribui",
  "const FORMATOS = ['Stories', 'Reels', 'Post único', 'Carrossel'];\n"
  "const paraFormato = f => { const n = String(f).toLowerCase(); if (FORMATOS.includes(f)) return f; if (n.includes('stor')) return 'Stories'; if (n.includes('carross')) return 'Carrossel'; if (/reel|v[ií]deo|short|live/.test(n)) return 'Reels'; return 'Post único'; };\n"
  "// NETWORKS aponta para state.networks (editável); migrate() reatribui")
t("formats: ['Post', 'Vídeo'], limit: 2200 };", "formats: [...FORMATOS], limit: 2200 };")

# Lista: ordem arrastada (pedido do Samuel, 26/11/2026). p.lorder guarda a posição; a ordem padrão da lista é a arrastada,
# e quem ainda não foi arrastado segue pela data, como antes.
t("    date: byDate,\n    time:", "    manual: (a, b) => ((a.lorder ?? 1e15) - (b.lorder ?? 1e15)) || byDate(a, b),\n    date: byDate,\n    time:")
t("group: 'none', sort: 'date', dir: 1,", "group: 'none', sort: 'manual', dir: 1,")

# Data e horário na lista: a data muda a cada parte digitada (dia, mês, ano), e redesenhar a lista a cada uma
# tirava o foco do campo no meio da digitação. Agora grava na hora e só redesenha quando o campo perde o foco.
t("  touch(p); save(); renderListBody(); renderSidebar();\n}\nfunction onPropField(el) {",
  "  if ((f === 'date' || f === 'time') && document.activeElement === el) {\n"
  "    touch(p); save();\n"
  "    if (!el.dataset.espera) { el.dataset.espera = '1'; el.addEventListener('blur', () => { delete el.dataset.espera; renderListBody(); renderSidebar(); }, { once: true }); }\n"
  "    return;\n"
  "  }\n"
  "  touch(p); save(); renderListBody(); renderSidebar();\n}\nfunction onPropField(el) {")
open('base.html', 'w', encoding='utf-8').write(s)
print('base.html gerado')

# Lista: barra de rolagem sempre visível, a de baixo sempre na tela (a tabela rola dentro de uma caixa da altura da janela).
CSS = """
.ltable-wrap{overflow-x:auto!important;scrollbar-color:auto;scrollbar-width:auto}
.ltable-wrap::-webkit-scrollbar{width:12px!important;height:12px!important;display:block}
.ltable-wrap::-webkit-scrollbar-thumb{background:color-mix(in srgb,var(--muted) 70%,transparent);border-radius:99px;border:3px solid var(--panel)}
.ltable-wrap::-webkit-scrollbar-thumb:hover{background:var(--muted)}
.ltable-wrap::-webkit-scrollbar-track{background:var(--hover)}
.ltable-wrap::-webkit-scrollbar-corner{background:var(--panel)}
"""
s = open('base.html', encoding='utf-8').read()
assert s.count('</style>') >= 1
s = s.replace('</style>', CSS + '</style>', 1)
open('base.html', 'w', encoding='utf-8').write(s)
print('css da lista posto')

# Barra de rolagem lateral própria, em cima da tabela: no Mac a barra nativa fica escondida até rolar com o trackpad.
JS = """
<script>
(function () {
  const css = document.createElement('style');
  css.textContent = '.lrolo{display:flex;align-items:center;gap:10px;margin:0 0 8px;font:600 12px system-ui;color:var(--muted)}' +
    '.lrolo input{flex:1;accent-color:var(--accent);height:18px;cursor:pointer}' +
    '.lcaixa{display:flex;gap:8px;align-items:stretch}.lcaixa>.ltable-wrap{flex:1;min-width:0}' +
    '.lvert{display:flex;flex-direction:column;align-items:center;gap:6px;width:30px;max-height:calc(100vh - 300px);position:sticky;top:12px}' +
    '.lvert input{flex:1;writing-mode:vertical-lr;direction:ltr;width:18px;accent-color:var(--accent);cursor:pointer;margin:0}' +
    '.lvert button,.lrolo button{border:1px solid var(--border);background:var(--panel);color:var(--text);border-radius:8px;width:30px;height:26px;cursor:pointer;font-size:14px}';
  document.head.appendChild(css);
  function ligar(w) {
    if (w.dataset.rolo) return; w.dataset.rolo = '1';
    const bar = document.createElement('div'); bar.className = 'lrolo';
    bar.innerHTML = '<span>Rolar para o lado</span><button type="button" data-d="-1" title="Para a esquerda">◀</button><input type="range" min="0" max="1000" value="0" aria-label="Rolar a tabela para o lado"><button type="button" data-d="1" title="Para a direita">▶</button>';
    w.parentNode.insertBefore(bar, w);
    const r = bar.querySelector('input');
    const max = () => Math.max(0, w.scrollWidth - w.clientWidth);
    const mostra = () => { bar.style.display = max() > 4 ? 'flex' : 'none'; r.value = max() ? Math.round(w.scrollLeft / max() * 1000) : 0; };
    r.addEventListener('input', () => { w.scrollLeft = r.value / 1000 * max(); });
    bar.querySelectorAll('button').forEach(b => b.addEventListener('click', () => { w.scrollBy({ left: Number(b.dataset.d) * w.clientWidth * 0.6, behavior: 'smooth' }); }));
    w.addEventListener('scroll', mostra);
    new ResizeObserver(mostra).observe(w);
    new MutationObserver(mostra).observe(w, { childList: true, subtree: true });
    mostra();
  }
  new MutationObserver(() => document.querySelectorAll('.ltable-wrap').forEach(ligar)).observe(document.body, { childList: true, subtree: true });
  document.querySelectorAll('.ltable-wrap').forEach(ligar);
})();
</script>
"""
s = open('base.html', encoding='utf-8').read()
i = s.rindex('</body>')
s = s[:i] + JS + s[i:]
open('base.html', 'w', encoding='utf-8').write(s)
print('rolagem lateral posta')

# Cor e ícone de cada formato (patch do Kivuli)
import subprocess, sys as _sys
subprocess.run([_sys.executable, 'formatos.py', 'base.html'], check=True)

# Barra vertical visível também nos menus (seletor de rede, formato, etapa, tags): no Mac a nativa fica escondida.
JS2 = """
<script>
(function () {
  const css = document.createElement('style');
  css.textContent = '.mbarra{position:fixed;z-index:101;width:16px;display:flex;flex-direction:column;align-items:center;gap:2px}' +
    '.mbarra input{flex:1;writing-mode:vertical-lr;direction:ltr;width:14px;margin:0;accent-color:var(--accent);cursor:pointer}' +
    '.mbarra button{border:0;background:transparent;color:var(--muted);font-size:10px;line-height:1;cursor:pointer;padding:2px}';
  document.head.appendChild(css);
  const ligados = new Map();
  function ligar(el) {
    if (ligados.has(el)) return;
    const b = document.createElement('div'); b.className = 'mbarra';
    b.innerHTML = '<button type="button" data-v="-1" title="Para cima">▲</button><input type="range" min="0" max="1000" value="0" aria-label="Rolar a lista para cima e para baixo"><button type="button" data-v="1" title="Para baixo">▼</button>';
    document.body.appendChild(b);
    const r = b.querySelector('input');
    const max = () => Math.max(0, el.scrollHeight - el.clientHeight);
    r.addEventListener('input', () => { el.scrollTop = r.value / 1000 * max(); });
    b.addEventListener('mousedown', e => e.preventDefault());
    b.querySelectorAll('button').forEach(x => x.addEventListener('click', e => { e.stopPropagation(); el.scrollBy({ top: Number(x.dataset.v) * el.clientHeight * 0.6, behavior: 'smooth' }); }));
    ligados.set(el, { b, r, max });
  }
  // Menu aberto perto do pé da janela: sobe até caber; se não couber, encolhe e ganha a barra.
  function caber(m) {
    const q = m.getBoundingClientRect(), H = innerHeight, folga = 10;
    if (q.bottom <= H - folga) return;
    const alto = m.scrollHeight + 2;
    if (alto <= H - 2 * folga) { m.style.top = (H - folga - alto) + 'px'; m.style.maxHeight = ''; }
    else { m.style.top = folga + 'px'; m.style.maxHeight = (H - 2 * folga) + 'px'; }
  }
  function atualizar() {
    document.querySelectorAll('.menu').forEach(caber);
    document.querySelectorAll('.menu, .op-list').forEach(el => { if (el.scrollHeight - el.clientHeight > 4) ligar(el); });
    for (const [el, o] of ligados) {
      if (!document.body.contains(el)) { o.b.remove(); ligados.delete(el); continue; }
      const m = o.max(); if (m <= 4) { o.b.style.display = 'none'; continue; }
      const q = el.getBoundingClientRect();
      Object.assign(o.b.style, { display: 'flex', left: (q.right - 18) + 'px', top: (q.top + 4) + 'px', height: Math.max(60, q.height - 8) + 'px' });
      o.r.value = Math.round(el.scrollTop / m * 1000);
    }
    requestAnimationFrame(atualizar);
  }
  requestAnimationFrame(atualizar);
})();
</script>
"""
s = open('base.html', encoding='utf-8').read()
i = s.rindex('</body>')
s = s[:i] + JS2 + s[i:]
open('base.html', 'w', encoding='utf-8').write(s)
print('barra dos menus posta')

# Arrastar linha da lista: alça ⋮⋮ em cada linha, linha de destino marcada, e a ordem grava em p.lorder.
JS3 = """
<script>
(function () {
  const css = document.createElement('style');
  css.textContent = '.lrow{position:relative}.lalca{position:absolute;left:2px;top:50%;transform:translateY(-50%);width:18px;height:26px;display:grid;place-items:center;cursor:grab;color:var(--muted);opacity:.35;font-size:14px;letter-spacing:-2px;user-select:none;z-index:2}' +
    '.lalca + .lc{padding-left:22px}.ltable:has(.lalca) .lhead>.lh:first-child{padding-left:30px}.lrow:hover .lalca{opacity:1}.lalca:active{cursor:grabbing}' +
    '.lrow.arrastando{opacity:.4}.lrow.alvo-cima{box-shadow:inset 0 3px 0 var(--accent)}.lrow.alvo-baixo{box-shadow:inset 0 -3px 0 var(--accent)}' +
    '.lordem{display:flex;align-items:center;gap:10px;margin:0 0 8px;font:500 13px system-ui;color:var(--muted)}' +
    '.lordem button{border:1px solid var(--border);background:var(--panel);color:var(--text);border-radius:8px;padding:4px 10px;cursor:pointer;font:600 12.5px system-ui}';
  document.head.appendChild(css);
  let arr = null, alvo = null, emCima = false;
  function limpa() { document.querySelectorAll('.lrow.alvo-cima,.lrow.alvo-baixo').forEach(r => r.classList.remove('alvo-cima', 'alvo-baixo')); }
  function ligarLinha(r) {
    if (r.querySelector(':scope > .lalca')) return;
    const h = document.createElement('div'); h.className = 'lalca'; h.textContent = '⋮⋮'; h.title = 'Arraste para mudar a ordem';
    h.draggable = true;
    h.addEventListener('dragstart', e => { arr = r.dataset.id; r.classList.add('arrastando'); e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', arr); try { e.dataTransfer.setDragImage(r, 20, 20); } catch (x) {} });
    h.addEventListener('dragend', () => { r.classList.remove('arrastando'); limpa(); arr = null; });
    r.prepend(h);
  }
  document.addEventListener('dragover', e => {
    if (!arr) return; const r = e.target.closest && e.target.closest('.lrow'); if (!r || r.dataset.id === arr) return;
    e.preventDefault(); e.dataTransfer.dropEffect = 'move';
    const q = r.getBoundingClientRect(); emCima = e.clientY < q.top + q.height / 2; alvo = r.dataset.id;
    limpa(); r.classList.add(emCima ? 'alvo-cima' : 'alvo-baixo');
  });
  document.addEventListener('drop', e => {
    if (!arr || !alvo) return; e.preventDefault(); limpa();
    const ids = [...document.querySelectorAll('.lrow[data-id]')].map(x => x.dataset.id).filter(id => id !== arr);
    let i = ids.indexOf(alvo); if (i < 0) return; if (!emCima) i++;
    ids.splice(i, 0, arr);
    // quem não está visível (filtro) mantém a posição relativa, depois dos visíveis
    const vis = new Set(ids); const resto = state.posts.filter(p => !vis.has(p.id)).sort((a, b) => (a.lorder ?? 1e15) - (b.lorder ?? 1e15));
    ids.forEach((id, k) => { const p = getPost(id); if (p) { if (p.lorder !== k) { p.lorder = k; touch(p); } } });
    resto.forEach((p, k) => { const n = ids.length + k; if (p.lorder !== undefined && p.lorder !== n) { p.lorder = n; touch(p); } });
    ui.list.sort = 'manual'; ui.list.dir = 1; arr = null; alvo = null;
    save(); renderListBody();
  });
  function aviso(w) {
    let a = w.parentNode.querySelector(':scope > .lordem');
    if (!a) { a = document.createElement('div'); a.className = 'lordem'; w.parentNode.insertBefore(a, w.parentNode.querySelector(':scope > .lrolo') || w); }
    const manual = ui.list.sort === 'manual';
    const txt = manual ? 'Arraste pela alça ⋮⋮, à esquerda da linha, para mudar a ordem.' : 'A lista está ordenada por uma coluna. Para arrastar, volte à ordem arrastada.';
    if (a.dataset.m !== String(manual)) {
      a.dataset.m = String(manual);
      a.innerHTML = '<span>' + txt + '</span>' + (manual ? '' : '<button type="button">Voltar à ordem arrastada</button>');
      const b = a.querySelector('button'); if (b) b.onclick = () => { ui.list.sort = 'manual'; ui.list.dir = 1; renderListBody(); };
    }
  }
  new MutationObserver(() => {
    const manual = typeof ui !== 'undefined' && ui.list && ui.list.sort === 'manual';
    document.querySelectorAll('.lrow[data-id]').forEach(r => { if (manual) ligarLinha(r); else r.querySelector(':scope > .lalca')?.remove(); });
    document.querySelectorAll('.ltable-wrap').forEach(aviso);
  }).observe(document.body, { childList: true, subtree: true });
})();
</script>
"""
s = open('base.html', encoding='utf-8').read()
i = s.rindex('</body>')
s = s[:i] + JS3 + s[i:]
open('base.html', 'w', encoding='utf-8').write(s)
print('arrastar na lista posto')

# Formatação ao selecionar texto, como no Notion (pedido do Samuel, 27/11/2026): negrito, itálico, sublinhado,
# tachado e marca-texto. O editor já guarda o HTML do bloco e o sanitize() já aceita B, I, U, S e MARK.
JS4 = """
<script>
(function () {
  const css = document.createElement('style');
  css.textContent = '.fbar{position:fixed;z-index:120;display:none;gap:2px;padding:4px;border-radius:10px;background:var(--c-tinta,#1C1B18);box-shadow:0 8px 24px rgba(0,0,0,.25)}' +
    '.fbar button{min-width:30px;height:30px;border:0;border-radius:7px;background:transparent;color:#F5F0E6;cursor:pointer;font:600 14px system-ui}' +
    '.fbar button:hover,.fbar button.on{background:rgba(255,255,255,.16)}' +
    '.editor .bc mark{background:#F7E27A;color:inherit;border-radius:3px;padding:0 2px}';
  document.head.appendChild(css);
  const bar = document.createElement('div'); bar.className = 'fbar';
  const B = [['bold', '<b>B</b>', 'Negrito (⌘B)'], ['italic', '<i>I</i>', 'Itálico (⌘I)'], ['underline', '<u>U</u>', 'Sublinhado (⌘U)'], ['strikeThrough', '<s>S</s>', 'Tachado'], ['mark', '🖍', 'Marca-texto'], ['limpar', '⌫', 'Tirar a formatação']];
  bar.innerHTML = B.map(([c, h, t]) => '<button type="button" data-c="' + c + '" title="' + t + '">' + h + '</button>').join('');
  document.body.appendChild(bar);
  let campo = null;
  function marcar() {
    const s = getSelection(); if (!s.rangeCount) return;
    const r = s.getRangeAt(0);
    const dentro = r.commonAncestorContainer.nodeType === 1 ? r.commonAncestorContainer : r.commonAncestorContainer.parentElement;
    const m = dentro.closest('mark');
    if (m) { m.replaceWith(...m.childNodes); return; }
    const el = document.createElement('mark');
    try { r.surroundContents(el); } catch (e) { el.appendChild(r.extractContents()); r.insertNode(el); }
  }
  bar.addEventListener('mousedown', e => e.preventDefault());
  bar.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || !campo) return;
    const c = b.dataset.c;
    if (c === 'mark') marcar();
    else if (c === 'limpar') { document.execCommand('removeFormat'); campo.querySelectorAll('mark').forEach(m => { if (getSelection().containsNode(m, true)) m.replaceWith(...m.childNodes); }); }
    else document.execCommand(c);
    campo.dispatchEvent(new InputEvent('input', { bubbles: true }));
    mostrar();
  });
  function mostrar() {
    const s = getSelection();
    const no = s.anchorNode && (s.anchorNode.nodeType === 1 ? s.anchorNode : s.anchorNode.parentElement);
    const el = no && no.closest('.editor .bc[contenteditable]');
    if (!el || s.isCollapsed || !s.toString().trim()) { bar.style.display = 'none'; campo = null; return; }
    campo = el;
    const q = s.getRangeAt(0).getBoundingClientRect();
    bar.style.display = 'flex';
    const w = bar.offsetWidth, h = bar.offsetHeight;
    bar.style.left = Math.max(8, Math.min(innerWidth - w - 8, q.left + q.width / 2 - w / 2)) + 'px';
    bar.style.top = (q.top - h - 8 < 8 ? q.bottom + 8 : q.top - h - 8) + 'px';
    bar.querySelectorAll('button').forEach(x => { const c = x.dataset.c; let on = false; try { on = ['bold', 'italic', 'underline', 'strikeThrough'].includes(c) && document.queryCommandState(c); } catch (e) {} x.classList.toggle('on', on); });
  }
  document.addEventListener('selectionchange', () => requestAnimationFrame(mostrar));
  addEventListener('scroll', () => { if (campo) mostrar(); }, true);
})();
</script>
"""
s = open('base.html', encoding='utf-8').read()
i = s.rindex('</body>')
s = s[:i] + JS4 + s[i:]
open('base.html', 'w', encoding='utf-8').write(s)
print('barra de formatação posta')
