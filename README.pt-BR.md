# Você não precisa do Obsidian

[English](README.md) | **Português (Brasil)**

Memória de longo prazo para agentes de IA (Claude Code, Codex, Gemini CLI e qualquer outro que leia arquivos) usando só uma pasta de arquivos Markdown. Sem programa instalado, sem banco de dados, sem assinatura. Cresce sem limite e funciona igual em todos os agentes.

## O problema

Todo agente lê, no começo de cada conversa, um arquivo de instruções ou de memória (`CLAUDE.md`, `MEMORY.md`, `AGENTS.md`, `GEMINI.md`). Esse arquivo tem limite de tamanho:

| Agente | O que é carregado | Limite (out/2026) |
|---|---|---|
| Claude Code | `MEMORY.md` da memória automática | primeiras 200 linhas ou 25 KB, o que vier antes |
| Codex CLI | `AGENTS.md` | 32 KB no total (`project_doc_max_bytes`) |
| Gemini CLI | `GEMINI.md` e importações | varia conforme a versão |

Os limites mudam; confira na documentação de cada um.

Quem guarda tudo num arquivo só acaba batendo no limite, e o agente passa a "esquecer" sem avisar: o fim do arquivo simplesmente não é lido.

A saída comum é instalar o Obsidian, um plugin de memória ou um banco vetorial. Nada disso resolve o problema de fato: o agente não usa a interface do Obsidian, só os arquivos `.md`, que qualquer editor de texto abre.

## A ideia: memória em camadas

O agente sempre lê um mapa pequeno e só abre o detalhe quando o assunto aparece. É como um livro: você não lê o livro inteiro para achar uma página, olha o sumário, vai ao capítulo e depois à página.

```
memory/
├── MEMORY.md                  camada 1: mapa das áreas (cerca de 10 linhas, não cresce)
├── _index-work.md             camada 2: uma linha por nota da área
├── _index-home.md
├── _index-computer.md
├── client-contract-acme.md    camada 3: notas, uma por fato
├── photo-backup.md
└── ...
```

| Camada | O que guarda | Quando o agente lê | Tamanho |
|---|---|---|---|
| 0. Regras | como você quer que ele trabalhe | sempre (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) | pequeno, fixo |
| 1. Mapa | as áreas e as palavras-chave de cada uma | sempre | cerca de 10 linhas, não cresce |
| 2. Sub-índice | título e resumo de uma linha de cada nota | quando o assunto é daquela área | sem limite prático |
| 3. Nota | o detalhe | quando é relevante | sem limite |

Rede de segurança: se o índice falhar, o agente procura pelo texto em todos os arquivos da pasta (`grep`). Isso dá conta de milhares de notas.

## Como começar (5 minutos)

1. Copie a pasta [`template/`](template) para onde quiser guardar a memória e apague as notas de exemplo.
2. Troque as áreas do `MEMORY.md` pelas suas (trabalho, casa, projetos...). Comece com poucas.
3. Ligue a pasta no seu agente (veja abaixo) e cole o conteúdo de [`template/MEMORY-RULES.md`](template/MEMORY-RULES.md) nas instruções dele, ajustando o caminho da pasta.
4. Já tem um `MEMORY.md` grande? Peça ao agente para migrar usando o [`MIGRATE-PROMPT.md`](MIGRATE-PROMPT.md).
5. De vez em quando, rode o verificador:

```
python tools/check.py caminho/da/memoria
```

Ele aponta nota fora do índice, link quebrado, nota sem descrição, conflito de sincronização e mapa grande demais. Só precisa do Python 3.8 ou mais novo.

Os arquivos do modelo estão em inglês para servir a qualquer pessoa, mas as notas podem ser escritas em português ou em qualquer língua. O que importa são os nomes dos arquivos e a estrutura. Se preferir as regras em português, peça ao agente para traduzir o `MEMORY-RULES.md`.

### Ligar no Claude Code

No `~/.claude/settings.json`, aponte a memória automática para a pasta:

```json
{ "autoMemoryDirectory": "/caminho/da/memoria" }
```

O Claude Code já carrega o `MEMORY.md` dessa pasta sozinho. Cole as regras no `~/.claude/CLAUDE.md` ou importe o arquivo com `@/caminho/da/memoria/MEMORY-RULES.md`.

Atenção: por padrão, o Claude Code é instruído a pôr uma linha no `MEMORY.md` para cada memória nova. As regras no `CLAUDE.md` têm prioridade e mandam essa linha para o sub-índice. Se escapar alguma, o verificador avisa.

### Ligar no Codex

O Codex lê `~/.codex/AGENTS.md` (ou o do `CODEX_HOME`) e não tem importação de arquivos. Cole nele as regras e o conteúdo do `MEMORY.md`. Como o mapa quase nunca muda, isso raramente precisa ser refeito.

### Ligar no Gemini CLI

No `~/.gemini/GEMINI.md`, importe os dois arquivos:

```
@/caminho/da/memoria/MEMORY-RULES.md
@/caminho/da/memoria/MEMORY.md
```

### Outros agentes

Qualquer agente que leia arquivos serve: aponte as instruções dele para as regras e o mapa.

## As regras que fazem funcionar

1. **Uma nota por fato**, com o cabeçalho `description:` de uma linha. É pela descrição que o agente decide se abre a nota.
2. **Atualizar em vez de duplicar:** antes de criar, procurar nota do mesmo assunto.
3. **Gravar na hora** em que aprendeu, não no fim da conversa, porque a conversa pode acabar antes.
4. **Datas absolutas** (`2026-10-28`, nunca "ontem").
5. **Nota nova vai no sub-índice, nunca no mapa.** O mapa só ganha linha quando surge uma área nova.
6. **Faxina de tempos em tempos:** juntar notas repetidas e corrigir ou apagar as erradas. Peça ao próprio agente.
7. **Nada de senha, token ou chave** na memória. A pasta costuma ir para nuvem e backup.

## Vários agentes, vários computadores

- **Uma fonte só:** as regras ficam em um arquivo, e o `CLAUDE.md`, o `AGENTS.md` e o `GEMINI.md` só apontam para ele (ou são copiados dele). Mudou a regra, muda em um lugar.
- **Mesma pasta para todos:** os agentes leem e gravam a mesma memória. O que um aprende, o outro já sabe.
- **Sincronização:** Syncthing, Git, Dropbox ou Nextcloud levam a pasta para os outros computadores. Se aparecer arquivo de conflito (`*.sync-conflict-*`), peça ao agente para juntar e apagar.

## Perguntas comuns

**Então o Obsidian é inútil?**
Para você ler e navegar, ele é ótimo, e pode abrir esta mesma pasta (os links `[[nome]]` funcionam nele). Para o agente, não acrescenta nada. Se você acha ele pesado, o Bloco de Notas, o VS Code ou qualquer editor servem.

**E banco vetorial / RAG?**
Só compensa com dezenas de milhares de notas ou com documentos longos. Para memória pessoal, a busca por texto é mais simples, mais previsível e não depende de nada instalado.

**Por que não deixar o agente decidir sozinho o que guardar?**
Ele decide, mas sem estrutura o arquivo cresce até ser cortado. As camadas só dão um lugar certo para cada coisa (e deixar a IA fazer absolutamente tudo custa dinheiro).

**Quanto isso aguenta?**
O mapa fica do mesmo tamanho para sempre. Se um sub-índice ficar grande demais (centenas de linhas), divida a área em duas.

## Licença

MIT. Veja [LICENSE](LICENSE).
