# Monta index.html a partir de original.html: troca o armazenamento local pelo do Google (Apps Script).
# Uso: python3 montar.py <URL do app da web do Apps Script>
import sys
URL = sys.argv[1] if len(sys.argv) > 1 else ''
s = open('original.html', encoding='utf-8').read()
def troca(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a)); s = s.replace(a, b)
troca("const ok = await DB.set('state', JSON.parse(JSON.stringify(state)));",
      "const ok = await Nuvem.gravar(JSON.parse(JSON.stringify(state)));")
troca("const stored = await DB.get('state');", "const stored = await Nuvem.abrir(await DB.get('state'));")
troca("`${icon('check', 12)} Salvo neste navegador`", "`${icon('check', 12)} ${Nuvem.ativa ? 'Salvo para a equipe' : 'Salvo só neste navegador'}`")
troca("${icon('check', 12)} Salvo neste navegador</div>", "${icon('check', 12)} ${Nuvem.ativa ? 'Salvo para a equipe' : 'Salvo só neste navegador'}</div>")
NUVEM = r'''
/* ---------------- nuvem (Google Apps Script): todos veem o mesmo ---------------- */
const NUVEM_URL = '__URL__';
const Nuvem = {
  rev: null, ativa: false,
  chave() {
    let c = localStorage.getItem('socialos-chave');
    if (!c) { c = prompt('Senha do SocialOS da equipe:') || ''; localStorage.setItem('socialos-chave', c); }
    return c;
  },
  async ler(so) {
    const r = await fetch(NUVEM_URL + '?chave=' + encodeURIComponent(this.chave()) + (so ? '&so=rev' : ''));
    const j = await r.json();
    if (j.erro === 'senha') { localStorage.removeItem('socialos-chave'); throw new Error('senha'); }
    return j;
  },
  async abrir(local) {
    if (!NUVEM_URL.startsWith('https://')) return local;
    for (let t = 0; t < 3; t++) {
      try {
        const j = await this.ler();
        this.ativa = true; this.rev = j.rev;
        if (j.state) { await DB.set('state', j.state); return j.state; }
        if (local) await this.gravar(local);
        return local;
      } catch (e) { if (e.message !== 'senha') break; alert('Senha errada. Tente de novo.'); }
    }
    this.ativa = false;
    setTimeout(() => toast('Sem conexão com a pasta da equipe: o que fizer agora fica só neste navegador.'), 800);
    return local;
  },
  async gravar(st) {
    await DB.set('state', st);
    if (!this.ativa) return true;
    try {
      const r = await fetch(NUVEM_URL, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({ chave: this.chave(), base: this.rev, state: st }) });
      const j = await r.json();
      if (j.conflito) {
        this.rev = j.rev; state = migrate(j.state || st); await DB.set('state', state); route();
        toast('Outra pessoa salvou antes: a tela mostra a versão dela. Refaça a sua última alteração.');
        return true;
      }
      if (j.erro) return false;
      this.rev = j.rev; return true;
    } catch { return false; }
  },
  async vigiar() {
    if (!this.ativa || dirty || document.hidden || ui.drag || ui.postId) return;
    const ativo = document.activeElement;
    if (ativo && /^(INPUT|TEXTAREA|SELECT)$/.test(ativo.tagName) || (ativo && ativo.isContentEditable)) return;
    try {
      const j = await this.ler(true);
      if (j.rev === this.rev) return;
      const k = await this.ler();
      if (dirty) return;
      this.rev = k.rev; state = migrate(k.state); await DB.set('state', state); route();
    } catch { }
  },
};
setInterval(() => Nuvem.vigiar(), 15000);
document.addEventListener('visibilitychange', () => { if (!document.hidden) Nuvem.vigiar(); });

'''.replace('__URL__', URL)
troca("/* ---------------- boot ---------------- */", NUVEM + "/* ---------------- boot ---------------- */")
open('index.html', 'w', encoding='utf-8').write(s)
print('index.html montado', 'com nuvem' if URL else 'SEM URL (só local)')
