# PROPOSTA para a Imara (não roda no app): marca cada formato com data-fmt para o CSS dar cor e ícone.
# Roda sobre o base.html, depois do multi.py e antes do montar.py. Mesmo estilo de troca do multi.py.
import sys
arq = sys.argv[1] if len(sys.argv) > 1 else 'base.html'
s = open(arq, encoding='utf-8').read()
def t(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
t("const fmtText = p => fmts(p).join(' + ');\n",
  "const fmtText = p => fmts(p).join(' + ');\n"
  "const FMT_SLUG = { 'Stories': 'stories', 'Reels': 'reels', 'Post único': 'post', 'Carrossel': 'carrossel' };\n"
  "const FMT_COR = { 'Stories': '#B4540F', 'Reels': '#7A4BB0', 'Post único': '#24658A', 'Carrossel': '#3D7A3A' };\n"
  "const fmtChips = p => `<span class=\"fmts\">${fmts(p).map(f => `<span class=\"fmt\" data-fmt=\"${FMT_SLUG[f] || 'outro'}\">${esc(f)}</span>`).join('')}</span>`;\n")
# Dashboard (próximos posts), card do Kanban, célula da Lista e propriedade do post
t("<div class=\"pmeta\">${netBadges(p)}<span>${esc(fmtText(p))}</span>", "<div class=\"pmeta\">${netBadges(p)}${fmtChips(p)}")
t("<div class=\"card-meta\">${netBadges(p)}<span class=\"tag\">${esc(fmtText(p))}</span>", "<div class=\"card-meta\">${netBadges(p)}${fmtChips(p)}")
t("title=\"Escolher um ou mais formatos\">${esc(fmtText(p))}</button>", "title=\"Escolher um ou mais formatos\">${fmtChips(p)}</button>", 2)
# Calendário: só o ícone do formato, antes do título
t("title=\"${esc(netNames(p) + ' · ' + fmtText(p) + ' · ", "title=\"${esc(netNames(p) + ' · ' + fmtText(p) + ' · ")
i = s.index("title=\"${esc(netNames(p) + ' · ' + fmtText(p) + ' · ")
j = s.index('<span class="chip-t">', i)
s = s[:j] + '${fmtChips(p)}' + s[j:]
# Seletor de formato: cada um na sua cor
t("list: () => FORMATOS.map(f => ({ id: f, name: f, color: '#94a3b8' }))", "list: () => FORMATOS.map(f => ({ id: f, name: f, color: FMT_COR[f] || '#94a3b8' }))")
open(arq, 'w', encoding='utf-8').write(s)
print('formatos marcados com data-fmt')
