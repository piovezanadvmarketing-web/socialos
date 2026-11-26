# Gera base.html a partir de original.html: o post passa a ter várias redes (p.networks) e vários formatos (p.formats).
# p.network e p.format continuam como o primeiro de cada lista, para a cor, o limite de caracteres e o que já existia.
s = open('original.html', encoding='utf-8').read()
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
open('base.html', 'w', encoding='utf-8').write(s)
print('base.html gerado')

# Lista: barra de rolagem sempre visível, a de baixo sempre na tela (a tabela rola dentro de uma caixa da altura da janela).
CSS = """
.ltable-wrap{overflow:auto;max-height:calc(100vh - 230px);scrollbar-color:auto;scrollbar-width:auto}
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
    '.lrolo button{border:1px solid var(--border);background:var(--panel);color:var(--text);border-radius:8px;width:30px;height:26px;cursor:pointer;font-size:14px}';
  document.head.appendChild(css);
  function ligar(w) {
    if (w.previousElementSibling && w.previousElementSibling.classList.contains('lrolo')) return;
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
