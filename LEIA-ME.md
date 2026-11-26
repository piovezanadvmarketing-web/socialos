# SocialOS da equipe

O SocialOS (planejamento de posts) com os dados guardados no Google, para quem abre o link ver o mesmo que a outra pessoa.

- **Onde abre:** pelo GitHub Pages (`index.html`). Pede a senha da equipe uma vez em cada navegador.
- **Onde ficam os dados:** num arquivo `SocialOS - dados.json` no Drive da conta do marketing, gravado pelo projeto do Apps Script "SocialOS - dados da equipe" (`Codigo.gs`), publicado como app da Web.
- **Sincronia:** cada alteração vai ao Google em menos de 1 segundo; a outra tela confere a cada 15 segundos e quando volta para a aba. Se as duas pessoas salvam ao mesmo tempo, a segunda vê a versão da primeira e refaz a alteração.
- **Montar de novo:** `python3 montar.py "<URL do app da Web>"` refaz o `index.html` a partir do `original.html` (o arquivo que veio, fora do git).
- **Fora do git:** a senha (`senha.txt`), a URL (`url.txt`), o original e o `set-chave.html` de teste.
