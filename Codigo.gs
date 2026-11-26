// SocialOS — guarda o estado do app num arquivo JSON do Drive de quem publica este script.
// Senha em Propriedades do script: CHAVE. Cada gravação aumenta REV; quem grava em cima de versão velha recebe "conflito".
const NOME = 'SocialOS - dados.json';

function arquivo_() {
  const p = PropertiesService.getScriptProperties();
  let id = p.getProperty('ARQUIVO');
  if (id) { try { return DriveApp.getFileById(id); } catch (e) {} }
  const f = DriveApp.createFile(NOME, 'null', 'application/json');
  p.setProperty('ARQUIVO', f.getId());
  return f;
}
function saida_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function chaveOk_(c) { const k = PropertiesService.getScriptProperties().getProperty('CHAVE'); return !!k && c === k; }
function rev_() { return Number(PropertiesService.getScriptProperties().getProperty('REV') || 0); }

function doGet(e) {
  if (!chaveOk_(e.parameter.chave)) return saida_({ erro: 'senha' });
  if (e.parameter.so === 'rev') return saida_({ rev: rev_() });
  return saida_({ rev: rev_(), state: JSON.parse(arquivo_().getBlob().getDataAsString() || 'null') });
}

function doPost(e) {
  let c; try { c = JSON.parse(e.postData.contents); } catch (x) { return saida_({ erro: 'formato' }); }
  if (!chaveOk_(c.chave)) return saida_({ erro: 'senha' });
  const trava = LockService.getScriptLock(); trava.waitLock(20000);
  try {
    const atual = rev_(), f = arquivo_();
    if (c.base !== atual) return saida_({ conflito: true, rev: atual, state: JSON.parse(f.getBlob().getDataAsString() || 'null') });
    f.setContent(JSON.stringify(c.state));
    PropertiesService.getScriptProperties().setProperty('REV', String(atual + 1));
    return saida_({ rev: atual + 1 });
  } finally { trava.releaseLock(); }
}

// Rode uma vez pelo editor: cria a senha da equipe (se ainda não houver) e a mostra no registro de execução.
function criarSenha() {
  const p = PropertiesService.getScriptProperties();
  if (!p.getProperty('CHAVE')) p.setProperty('CHAVE', Utilities.getUuid().slice(0, 8));
  arquivo_();
  console.log('SENHA DA EQUIPE: ' + p.getProperty('CHAVE'));
}
