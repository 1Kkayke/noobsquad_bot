# 🎵 NoobSquad Discord Bot

Bot multifuncional para Discord com funcionalidades avançadas de música (YouTube) e monitoramento de canais (YouTube e Twitch).

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Comandos Disponíveis](#-comandos-disponíveis)
- [Arquitetura](#-arquitetura)
- [Troubleshooting](#-troubleshooting)
- [Desenvolvimento](#-desenvolvimento)
- [Licença](#-licença)

## ✨ Funcionalidades

### 🎵 Sistema de Música
- ▶️ Reprodução de músicas e playlists do YouTube
- 📋 Sistema de fila avançado com suporte para múltiplas operações
- 🎚️ Presets de equalização (padrão, pop, rock, graves)
- 🔄 Auto-play de músicas recomendadas baseado no histórico
- ⏸️ Controles completos: play, pause, resume, skip, stop
- 🔀 Embaralhamento de fila
- 📊 Perfil musical personalizado por usuário
- 💡 Sistema de recomendações baseado em preferências
- 📜 Histórico de reprodução persistente

### 📺 Sistema de Monitoramento
- 🎥 Monitoramento de canais do YouTube (notificações de novos vídeos)
- 🔴 Monitoramento de canais da Twitch (notificações de lives)
- 👤 Sistema de assinaturas por usuário
- 🔔 Notificações em tempo real com embeds ricos
- 📝 Gerenciamento de inscrições (adicionar/remover/listar)

### 🗄️ Persistência de Dados
- 💾 Banco de dados MongoDB para armazenamento
- 👥 Perfis de usuário individuais
- 📊 Estatísticas e preferências musicais
- 🎯 Sistema de recomendações inteligente

## 🔧 Pré-requisitos

### Software Necessário
- **Python 3.8+** (recomendado: Python 3.11)
- **FFmpeg** (para reprodução de áudio)
- **MongoDB** (pode usar Docker)
- **Git** (para clonar o repositório)

### APIs Necessárias

#### Obrigatórias
- **Discord Bot Token**: [Discord Developer Portal](https://discord.com/developers/applications)
- **MongoDB**: Conexão local ou [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

#### Opcionais (para funcionalidades específicas)
- **YouTube API Key**: [Google Cloud Console](https://console.cloud.google.com/apis/credentials) (para monitoramento de canais)
- **Twitch API**: [Twitch Developers](https://dev.twitch.tv/console/apps) (para monitoramento de lives)

## 📦 Instalação

### Opção 1: Docker (Recomendado)

1. **Clone o repositório**
```bash
git clone https://github.com/1Kkayke/noobsquad_bot.git
cd noobsquad_bot
```

2. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. **Execute com Docker Compose**
```bash
docker-compose up -d
```

### Opção 2: Instalação Local

1. **Clone o repositório**
```bash
git clone https://github.com/1Kkayke/noobsquad_bot.git
cd noobsquad_bot
```

2. **Instale o FFmpeg**

**Windows:**
- Baixe de [ffmpeg.org](https://ffmpeg.org/download.html)
- Adicione ao PATH do sistema

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

3. **Crie e ative um ambiente virtual**
```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. **Configure o MongoDB**
- Instale localmente ou use MongoDB Atlas
- Configure a string de conexão no arquivo `.env`

6. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

7. **Execute o bot**
```bash
python bot/main.py
```

## ⚙️ Configuração

### 1. Criar o Bot no Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application" e dê um nome ao bot
3. Vá em "Bot" no menu lateral e clique em "Add Bot"
4. Em "TOKEN", clique em "Reset Token" e copie o token
5. Ative as seguintes "Privileged Gateway Intents":
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
6. Vá em "OAuth2" > "URL Generator"
7. Selecione os scopes:
   - ✅ bot
   - ✅ applications.commands
8. Selecione as permissões:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Connect (voz)
   - ✅ Speak (voz)
9. Copie a URL gerada e use para adicionar o bot ao seu servidor

### 2. Configurar IDs dos Canais

1. Ative o "Modo Desenvolvedor" no Discord:
   - Configurações do Usuário > Avançado > Modo Desenvolvedor
2. Clique com botão direito no canal desejado e selecione "Copiar ID"
3. Configure no arquivo `.env`:
   - `CHAT_JUKEBOX`: Canal onde comandos de música funcionarão
   - `REBOOT_CHANNEL_ID`: Canal para notificações de reinício (opcional)
   - `NOTIFICATION_CHANNEL_ID`: Canal para notificações de monitoramento (opcional)

### 3. Configurar APIs (Opcional)

#### YouTube API
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a "YouTube Data API v3"
4. Vá em "Credenciais" e crie uma "Chave de API"
5. Copie a chave e adicione no `.env` como `YOUTUBE_API_KEY`

#### Twitch API
1. Acesse [Twitch Developers](https://dev.twitch.tv/console/apps)
2. Clique em "Register Your Application"
3. Preencha os dados e defina a OAuth Redirect URL
4. Copie o "Client ID" e "Client Secret"
5. Adicione no `.env` como `TWITCH_CLIENT_ID` e `TWITCH_CLIENT_SECRET`

### 4. Arquivo .env Completo

```env
# Discord Configuration (REQUIRED)
DISCORD_TOKEN=seu_token_aqui
CHAT_JUKEBOX=123456789012345678
REBOOT_CHANNEL_ID=0
NOTIFICATION_CHANNEL_ID=0

# MongoDB Configuration (REQUIRED)
MONGODB_URI=mongodb://localhost:27017/noobsquad_bot
DATABASE_NAME=noobsquad_bot

# YouTube API (OPTIONAL - only for monitoring)
YOUTUBE_API_KEY=

# Twitch API (OPTIONAL - only for monitoring)
TWITCH_CLIENT_ID=
TWITCH_CLIENT_SECRET=

# Monitoring Configuration
CHECK_YOUTUBE_INTERVAL=300
CHECK_TWITCH_INTERVAL=180
```

## 🎮 Comandos Disponíveis

### 🎵 Comandos de Música

| Comando | Aliases | Descrição | Exemplo |
|---------|---------|-----------|---------|
| `!play <url>` | - | Toca uma música ou playlist do YouTube | `!play https://youtube.com/watch?v=...` |
| `!play <url> autoplay` | - | Ativa o modo autoplay | `!play https://... autoplay` |
| `!pause` | - | Pausa a música atual | `!pause` |
| `!resume` | - | Retoma a música pausada | `!resume` |
| `!skip` | - | Pula para a próxima música | `!skip` |
| `!stop` | - | Para a música atual | `!stop` |
| `!leave` | - | Desconecta o bot do canal de voz | `!leave` |
| `!queue` | `!fila`, `!q` | Mostra a fila de músicas | `!queue` |
| `!nowplaying` | `!np`, `!tocando` | Mostra a música atual | `!np` |
| `!clear` | `!limpar` | Limpa toda a fila | `!clear` |
| `!shuffle` | `!embaralhar` | Embaralha a fila | `!shuffle` |
| `!profile` | - | Mostra seu perfil musical | `!profile` |
| `!recommend` | - | Recomendações baseadas no seu histórico | `!recommend` |
| `!reproduzir_historico` | - | Adiciona músicas do histórico à fila | `!reproduzir_historico 10` |

#### Detalhes do comando `!reproduzir_historico`

```
!reproduzir_historico [count] [flags]

Parâmetros:
  count: Número de músicas do histórico (padrão: 5)
  
Flags:
  append: Adiciona ao final da fila (senão, toca em seguida)
  search: Busca no YouTube se não houver URL no histórico

Exemplos:
  !reproduzir_historico              # 5 músicas, tocar em seguida
  !reproduzir_historico 10           # 10 músicas, tocar em seguida
  !reproduzir_historico 5 append     # 5 músicas, adicionar no fim
  !reproduzir_historico 8 search     # 8 músicas, buscar por título
  !reproduzir_historico 10 append search  # Combinar flags
```

### 📺 Comandos de Monitoramento

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `!monitorar_youtube <canal>` | Monitora um canal do YouTube | `!monitorar_youtube @nomedocanal` |
| `!monitorar_twitch <canal>` | Monitora um canal da Twitch | `!monitorar_twitch nomedocanal` |
| `!listar_monitoramento` | Lista seus canais monitorados | `!listar_monitoramento` |
| `!remover_monitoramento <plataforma> <canal>` | Remove um canal | `!remover_monitoramento youtube nomedocanal` |

### ❓ Comandos de Ajuda

| Comando | Descrição |
|---------|-----------|
| `!ajuda` | Mostra todos os comandos disponíveis |

## 🏗️ Arquitetura

### Estrutura do Projeto

```
noobsquad_bot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada do bot
│   ├── commands.py          # Agregador de comandos
│   ├── commands_music.py    # Comandos de música
│   ├── commands_monitor.py  # Comandos de monitoramento
│   ├── commands_help.py     # Comandos de ajuda
│   ├── commands_utils.py    # Utilitários compartilhados
│   ├── utils.py             # Funções auxiliares
│   ├── monitor.py           # Sistema de monitoramento
│   └── scheduler.py         # Agendamento de tarefas
├── config/
│   ├── __init__.py
│   └── settings.py          # Configurações e variáveis de ambiente
├── db/
│   ├── __init__.py
│   ├── database.py          # Conexão e operações do MongoDB
│   └── models.py            # Modelos de dados
├── .env.example             # Exemplo de configuração
├── .gitignore              # Arquivos ignorados pelo Git
├── Dockerfile              # Configuração do Docker
├── docker-compose.yml      # Orquestração de containers
├── entrypoint.sh           # Script de inicialização
├── requirements.txt        # Dependências Python
└── README.md               # Este arquivo
```

### Componentes Principais

#### 1. Sistema de Comandos (Cogs)
- **MusicCommands**: Gerencia todos os comandos relacionados à música
- **MonitorCommands**: Gerencia monitoramento de canais
- **HelpCommands**: Sistema de ajuda e documentação

#### 2. Banco de Dados
- **UserProfile**: Perfis de usuário com histórico e preferências
- **MonitoredChannel**: Canais monitorados com sistema de assinaturas
- **Song**: Representação de músicas no histórico
- **MusicPreference**: Preferências musicais por gênero/artista

#### 3. Sistema de Monitoramento
- **ChannelMonitor**: Interface com APIs do YouTube e Twitch
- **MonitorScheduler**: Verifica periodicamente atualizações de canais
- Sistema de notificações automáticas

#### 4. Sistema de Música
- Fila de reprodução por servidor (guild)
- Sistema de autoplay com recomendações
- Equalização com presets personalizados
- Integração com yt-dlp para extração de áudio

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Bot não conecta ao Discord

**Sintoma**: Erro "Token do bot não encontrado"

**Solução**:
- Verifique se o arquivo `.env` existe e está configurado
- Confirme que o token está correto no Discord Developer Portal
- Certifique-se de que não há espaços extras no token

#### 2. Músicas não tocam

**Sintoma**: Erro "DownloadError" ou "Falha ao obter URL de stream"

**Solução**:
```bash
# Atualize o yt-dlp
pip install --upgrade yt-dlp

# Em caso de problemas persistentes, reinstale
pip uninstall yt-dlp
pip install yt-dlp
```

#### 3. FFmpeg não encontrado

**Sintoma**: Erro relacionado ao FFmpeg ao tentar tocar música

**Solução**:
- Windows: Baixe de [ffmpeg.org](https://ffmpeg.org) e adicione ao PATH
- Linux: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

#### 4. MongoDB não conecta

**Sintoma**: Erro de conexão com MongoDB

**Solução**:
- Verifique se o MongoDB está rodando: `sudo systemctl status mongod`
- Confirme a string de conexão no `.env`
- Se usar Docker: `docker-compose ps` para verificar o status

#### 5. Monitoramento não funciona

**Sintoma**: Não recebe notificações de canais

**Solução**:
- Verifique se as APIs estão configuradas (YouTube/Twitch)
- Confirme que `NOTIFICATION_CHANNEL_ID` está configurado
- Verifique os logs para erros de autenticação da API

#### 6. Comando não funciona no canal

**Sintoma**: Bot responde "Use o canal JUKEBOX"

**Solução**:
- Configure `CHAT_JUKEBOX` no `.env` com o ID do canal correto
- Ative o Modo Desenvolvedor no Discord para copiar IDs
- Clique com botão direito no canal > Copiar ID

### Logs

Os logs são salvos automaticamente em arquivos com formato:
```
bot_log_YYYY-MM-DD.log
```

Para visualizar logs em tempo real:
```bash
tail -f bot_log_$(date +%Y-%m-%d).log
```

## 👨‍💻 Desenvolvimento

### Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Estilo de Código

- Seguimos PEP 8 para código Python
- Use docstrings para documentar funções e classes
- Adicione type hints quando possível
- Mantenha funções pequenas e focadas
- Escreva código auto-documentado

### Testando Localmente

1. Configure um servidor Discord de teste
2. Use IDs de canais do servidor de teste no `.env`
3. Teste cada comando individualmente
4. Verifique os logs para erros

### Adicionando Novos Comandos

1. Adicione o comando no Cog apropriado (`commands_music.py`, etc.)
2. Use decoradores `@commands.command()`
3. Adicione aliases se apropriado
4. Documente o comando com docstring
5. Adicione ao help em `commands_help.py`
6. Teste extensivamente

### Estrutura de um Comando

```python
@commands.command(name='meucomando', aliases=['mc'])
async def meu_comando(self, ctx, arg1: str, arg2: int = 10):
    """Descrição curta do comando
    
    Args:
        arg1: Descrição do argumento 1
        arg2: Descrição do argumento 2 (opcional, padrão: 10)
    
    Uso: !meucomando <arg1> [arg2]
    """
    try:
        # Validações
        if not ctx.author.voice:
            await ctx.send("Conecte-se a um canal de voz!")
            return
        
        # Lógica do comando
        resultado = processar_algo(arg1, arg2)
        
        # Resposta
        await ctx.send(f"✅ Comando executado: {resultado}")
        
    except Exception as e:
        logging.error(f"Erro no comando meucomando: {e}")
        await ctx.send("❌ Erro ao executar o comando.")
```

## 📝 Notas Adicionais

### Limitações da API do YouTube

- A API gratuita tem limite de 10.000 unidades/dia
- Cada busca consome aproximadamente 100 unidades
- Monitoramento frequente pode exceder o limite
- Considere aumentar o intervalo de verificação se necessário

### Limitações da API do Twitch

- Tokens OAuth expiram após algumas horas
- O bot reconecta automaticamente quando necessário
- Rate limits aplicam-se (800 requisições/minuto)

### Performance

- O bot usa conexão assíncrona para melhor performance
- MongoDB com índices para consultas rápidas
- Cache de informações de músicas em memória
- Limpeza automática de recursos ao desligar

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Suporte

Se você encontrar problemas ou tiver sugestões:

1. Verifique a seção [Troubleshooting](#-troubleshooting)
2. Procure em [Issues](https://github.com/1Kkayke/noobsquad_bot/issues) existentes
3. Abra um novo Issue se necessário
4. Forneça o máximo de detalhes possível:
   - Descrição do problema
   - Passos para reproduzir
   - Logs relevantes
   - Versão do Python e sistema operacional

## ⭐ Agradecimentos

- [discord.py](https://github.com/Rapptz/discord.py) - Biblioteca Discord
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Extração de vídeos
- [MongoDB](https://www.mongodb.com/) - Banco de dados
- Comunidade Discord - Suporte e feedback

---

Desenvolvido com ❤️ por [1Kkayke](https://github.com/1Kkayke)
