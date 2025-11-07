# 🤝 Contribuindo para o NoobSquad Discord Bot

Obrigado por considerar contribuir para o NoobSquad Discord Bot! Este documento fornece diretrizes para contribuições.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Posso Contribuir?](#como-posso-contribuir)
- [Diretrizes de Desenvolvimento](#diretrizes-de-desenvolvimento)
- [Processo de Pull Request](#processo-de-pull-request)
- [Estilo de Código](#estilo-de-código)
- [Mensagens de Commit](#mensagens-de-commit)

## 📜 Código de Conduta

Este projeto e todos os participantes devem aderir a um código de conduta respeitoso:

- Use linguagem acolhedora e inclusiva
- Seja respeitoso com pontos de vista e experiências diferentes
- Aceite críticas construtivas com elegância
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros da comunidade

## 🎯 Como Posso Contribuir?

### Reportando Bugs

Antes de criar um relatório de bug, verifique se o problema já não foi reportado. Se você encontrar um bug:

1. **Use o template de issue** para bugs
2. **Descreva o comportamento esperado** claramente
3. **Descreva o comportamento atual** em detalhes
4. **Forneça passos para reproduzir** o problema
5. **Inclua informações do ambiente**:
   - Versão do Python
   - Sistema operacional
   - Versão das dependências
6. **Adicione logs relevantes** (remova informações sensíveis)
7. **Adicione screenshots** se aplicável

#### Exemplo de Relatório de Bug

```markdown
**Descrição**
O bot não consegue tocar músicas do YouTube.

**Passos para Reproduzir**
1. Use o comando `!play https://youtube.com/watch?v=...`
2. O bot conecta ao canal de voz
3. Erro aparece no console

**Comportamento Esperado**
O bot deveria tocar a música.

**Comportamento Atual**
Erro: "DownloadError: HTTP Error 403: Forbidden"

**Ambiente**
- Python: 3.11.5
- OS: Windows 11
- yt-dlp: 2023.10.13

**Logs**
```
[2024-01-15 10:30:45] [ERROR] Erro ao extrair stream: HTTP Error 403
```
```

### Sugerindo Melhorias

Melhorias são sempre bem-vindas! Para sugerir uma melhoria:

1. **Verifique se já não foi sugerida** nas issues
2. **Descreva a melhoria** claramente
3. **Explique por que seria útil** para o projeto
4. **Forneça exemplos** de uso, se possível
5. **Considere alternativas** e mencione-as

### Contribuindo com Código

1. **Fork o repositório**
2. **Clone seu fork**
   ```bash
   git clone https://github.com/seu-usuario/noobsquad_bot.git
   cd noobsquad_bot
   ```

3. **Crie uma branch** para sua feature
   ```bash
   git checkout -b feature/minha-feature
   ```
   
   Nomeie a branch seguindo o padrão:
   - `feature/nome-da-feature` para novas funcionalidades
   - `fix/nome-do-bug` para correções
   - `docs/nome-da-doc` para documentação
   - `refactor/nome-do-refactor` para refatorações

4. **Configure o ambiente de desenvolvimento**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou .\.venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

5. **Faça suas alterações** seguindo o [estilo de código](#estilo-de-código)

6. **Teste suas alterações** extensivamente

7. **Commit suas mudanças** usando [mensagens apropriadas](#mensagens-de-commit)

8. **Push para sua branch**
   ```bash
   git push origin feature/minha-feature
   ```

9. **Abra um Pull Request** na branch principal

## 🛠️ Diretrizes de Desenvolvimento

### Estrutura do Projeto

Mantenha a organização do projeto:

```
bot/              # Código principal do bot
├── commands_*.py # Comandos organizados por categoria
├── main.py       # Ponto de entrada
├── monitor.py    # Sistema de monitoramento
└── utils.py      # Utilitários

config/           # Configurações
db/               # Modelos e database
```

### Adicionando Novos Comandos

1. **Adicione ao Cog apropriado** (`commands_music.py`, `commands_monitor.py`, etc.)

2. **Use a estrutura padrão**:
   ```python
   @commands.command(name='meucomando', aliases=['mc', 'alias'])
   async def meu_comando(self, ctx, arg1: str, arg2: int = 10):
       """Descrição curta do comando
       
       Args:
           arg1: Descrição do argumento
           arg2: Argumento opcional (padrão: 10)
       
       Uso: !meucomando <arg1> [arg2]
       Exemplo: !meucomando teste 20
       """
       try:
           # Validações
           if not validar_canal(ctx):
               await ctx.send("Use o canal correto!")
               return
           
           # Lógica do comando
           resultado = processar(arg1, arg2)
           
           # Resposta
           await ctx.send(f"✅ {resultado}")
           
       except Exception as e:
           logging.error(f"Erro em meucomando: {e}")
           await ctx.send("❌ Erro ao executar comando.")
   ```

3. **Adicione ao help** em `commands_help.py`

4. **Documente no README** se relevante

### Adicionando Dependências

1. **Instale a dependência**:
   ```bash
   pip install nova-biblioteca
   ```

2. **Atualize requirements.txt**:
   ```bash
   pip freeze | grep nova-biblioteca >> requirements.txt
   ```

3. **Documente o uso** da nova dependência

4. **Justifique no PR** por que a dependência é necessária

### Trabalhando com o Banco de Dados

1. **Use os modelos existentes** em `db/models.py`

2. **Adicione novos métodos** em `db/database.py` se necessário

3. **Mantenha a retrocompatibilidade** com dados existentes

4. **Documente mudanças no schema**

### Tratamento de Erros

- **Sempre use try-except** em comandos
- **Log erros** com `logging.error()`
- **Forneça mensagens úteis** ao usuário
- **Não exponha detalhes técnicos** sensíveis

Exemplo:
```python
try:
    resultado = operacao_arriscada()
    await ctx.send(f"✅ Sucesso: {resultado}")
except ValueError as e:
    logging.error(f"Valor inválido: {e}")
    await ctx.send("❌ Valor fornecido é inválido.")
except Exception as e:
    logging.error(f"Erro inesperado: {e}")
    await ctx.send("❌ Ocorreu um erro inesperado.")
```

## 🔄 Processo de Pull Request

### Antes de Submeter

- [ ] Código segue o [estilo do projeto](#estilo-de-código)
- [ ] Comentários úteis foram adicionados
- [ ] Documentação foi atualizada
- [ ] Mudanças foram testadas localmente
- [ ] Nenhum arquivo desnecessário foi incluído
- [ ] Commits seguem o [padrão](#mensagens-de-commit)

### Template de Pull Request

```markdown
## Descrição
Breve descrição das mudanças.

## Tipo de Mudança
- [ ] Bug fix (mudança que corrige um problema)
- [ ] Nova feature (mudança que adiciona funcionalidade)
- [ ] Breaking change (mudança que pode quebrar funcionalidade existente)
- [ ] Documentação

## Como Foi Testado?
Descreva os testes realizados.

## Checklist
- [ ] Código testado localmente
- [ ] Documentação atualizada
- [ ] Sem warnings ou erros
- [ ] Segue o estilo do projeto

## Screenshots (se aplicável)
Adicione screenshots para mudanças visuais.
```

### Revisão

- Seja paciente durante a revisão
- Responda a comentários de forma construtiva
- Faça as alterações solicitadas
- Marque conversas como resolvidas quando apropriado

## 📝 Estilo de Código

### Python (PEP 8)

- **Indentação**: 4 espaços (não tabs)
- **Linha máxima**: 120 caracteres (preferência 100)
- **Imports**: No topo do arquivo, organizados
- **Nomes**:
  - Classes: `PascalCase`
  - Funções/variáveis: `snake_case`
  - Constantes: `UPPER_SNAKE_CASE`

### Docstrings

Use docstrings para todas as funções públicas:

```python
def funcao_exemplo(arg1: str, arg2: int = 10) -> bool:
    """Descrição breve da função.
    
    Descrição mais detalhada se necessário.
    
    Args:
        arg1: Descrição do primeiro argumento
        arg2: Descrição do segundo argumento (opcional)
    
    Returns:
        True se sucesso, False caso contrário
    
    Raises:
        ValueError: Se arg1 estiver vazio
    """
    pass
```

### Type Hints

Use type hints sempre que possível:

```python
from typing import Optional, List, Dict

def processar_lista(items: List[str]) -> Optional[Dict[str, int]]:
    """Processa uma lista de items."""
    pass
```

### Comentários

- Comentários devem explicar **por que**, não **o que**
- Use comentários para lógica complexa
- Mantenha comentários atualizados com o código

```python
# BOM: Explica o motivo
# Aguardamos 5 segundos para evitar rate limiting da API
await asyncio.sleep(5)

# RUIM: Descreve o óbvio
# Aguarda 5 segundos
await asyncio.sleep(5)
```

### Organização de Imports

```python
# 1. Biblioteca padrão
import os
import logging
from datetime import datetime

# 2. Bibliotecas de terceiros
import discord
from discord.ext import commands

# 3. Imports locais
from config.settings import DISCORD_TOKEN
from db.database import db
```

## 💬 Mensagens de Commit

### Formato

```
<tipo>(<escopo>): <assunto>

<corpo>

<rodapé>
```

### Tipos

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças na documentação
- `style`: Formatação, pontos e vírgulas, etc
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Tarefas de manutenção

### Exemplos

```bash
feat(music): adiciona comando de volume

Implementa controle de volume com comando !volume.
Valores entre 0 e 100.

Closes #42
```

```bash
fix(monitor): corrige erro ao verificar canal do YouTube

O erro ocorria quando o canal não tinha vídeos recentes.
Adiciona validação antes de acessar items[0].

Fixes #38
```

```bash
docs(readme): atualiza seção de instalação

Adiciona instruções específicas para macOS.
```

### Diretrizes

- Use o imperativo ("adiciona" não "adicionado")
- Primeira linha com no máximo 50 caracteres
- Corpo com no máximo 72 caracteres por linha
- Referencie issues quando aplicável
- Seja descritivo mas conciso

## ❓ Dúvidas?

Se você tiver dúvidas sobre como contribuir:

1. Verifique a [documentação](README.md)
2. Procure em [Issues](https://github.com/1Kkayke/noobsquad_bot/issues)
3. Abra uma nova issue com a tag `question`

## 🙏 Agradecimentos

Obrigado por contribuir para o NoobSquad Discord Bot! Cada contribuição, por menor que seja, é muito apreciada.

---

**Nota**: Estas diretrizes podem ser atualizadas. Verifique periodicamente por mudanças.
