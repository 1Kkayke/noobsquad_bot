"""
NoobSquad Discord Bot - Ponto de Entrada Principal

Este módulo inicializa e executa o bot Discord com todas as suas funcionalidades:
- Sistema de música com reprodução do YouTube
- Monitoramento de canais do YouTube e Twitch
- Sistema de perfis de usuário e recomendações
- Integração com MongoDB para persistência de dados

Autor: 1Kkayke
Licença: MIT
"""

import discord
import logging
from datetime import datetime
from discord.ext import commands

from config.settings import (
    DISCORD_TOKEN,
    REBOOT_CHANNEL_ID
)
from db.database import db
from bot.commands import MusicCommands, HelpCommands
from bot.commands_monitor import MonitorCommands
from bot.scheduler import MonitorScheduler

# --- CONFIGURAÇÃO DE LOGGING ---
# Cria arquivo de log com a data atual para fácil identificação
log_filename = datetime.now().strftime('bot_log_%Y-%m-%d.log')
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Validação de token obrigatório
if not DISCORD_TOKEN:
    logging.error("Token do bot não encontrado no arquivo .env")
    raise ValueError("Token do bot não encontrado no arquivo .env")

# --- CONFIGURAÇÃO DAS INTENTS E BOT ---
# Intents permitem que o bot acesse eventos específicos do Discord
intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler conteúdo de mensagens
intents.voice_states = True     # Necessário para gerenciar estados de voz

# Cria a instância do bot com prefix '!' e timeout aumentado para estabilidade
bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    heartbeat_timeout=60.0,
    help_command=None  # Desativa comando help padrão (usamos customizado)
)

# Criar instância do scheduler para monitoramento de canais
scheduler = MonitorScheduler(bot)


# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
def setup_database():
    """Inicializa a conexão com o banco de dados MongoDB.
    
    Esta função:
    - Estabelece conexão com MongoDB
    - Cria índices necessários para performance
    - Valida que as coleções necessárias existem
    
    Raises:
        Exception: Se houver falha na conexão ou inicialização
    """
    try:
        db.connect()
        db.initialize_collections()  # Inicializa as coleções e índices
        logging.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao inicializar banco de dados: {e}")
        raise e


# --- REGISTRAR OS COGS ---
async def setup_cogs():
    """Configura e registra todos os Cogs (módulos de comandos) do bot.
    
    Cogs organizados por funcionalidade:
    - MusicCommands: Comandos de reprodução de música
    - MonitorCommands: Comandos de monitoramento de canais
    - HelpCommands: Sistema de ajuda
    
    O scheduler é iniciado após o registro dos Cogs para garantir
    que todas as dependências estejam prontas.
    """
    # Garante que o banco de dados está conectado antes de registrar os Cogs
    setup_database()

    await bot.add_cog(MusicCommands(bot))
    await bot.add_cog(MonitorCommands(bot))
    await bot.add_cog(HelpCommands(bot))

    # Iniciar o scheduler de monitoramento
    await scheduler.start()

    logging.info("Cogs registrados com sucesso!")


@bot.event
async def on_ready():
    """Evento disparado quando o bot está pronto e conectado ao Discord.
    
    Executado quando:
    - Bot se conecta pela primeira vez
    - Bot reconecta após desconexão
    
    Ações realizadas:
    - Registra todos os Cogs
    - Envia mensagem de reboot no canal configurado (se disponível)
    """
    await setup_cogs()  # Registra os Cogs quando o bot iniciar
    logging.info(f'Bot conectado como {bot.user.name}')

    try:
        # Reconectar ao canal de voz se o bot reiniciar
        if REBOOT_CHANNEL_ID:
            reboot_channel = bot.get_channel(REBOOT_CHANNEL_ID)
            if reboot_channel:
                await reboot_channel.send("🔄 Bot reiniciado e pronto para uso!")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem de reboot: {e}")


@bot.event
async def on_command_error(ctx, error):
    """Trata erros de comando globalmente.
    
    Args:
        ctx: Contexto do comando que gerou o erro
        error: Exceção que foi levantada
    
    Tipos de erros tratados:
    - CommandNotFound: Comando não existe
    - Outros: Erros genéricos são logados e informados ao usuário
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"🤔 Comando não encontrado. Digite `!ajuda` para ver a lista de comandos disponíveis.")
    else:
        # Para outros erros, loga e informa o usuário
        logging.error(f"Ocorreu um erro no comando '{ctx.command}': {error}")
        await ctx.send("❌ Ocorreu um erro ao processar o comando. Por favor, tente novamente.")


@bot.event
async def on_error(event, *args, **kwargs):
    """Tratamento global de erros não relacionados a comandos.
    
    Args:
        event: Nome do evento que gerou o erro
        *args: Argumentos posicionais do evento
        **kwargs: Argumentos nomeados do evento
    
    Loga todos os detalhes do erro para diagnóstico.
    """
    logging.error(f"Erro no evento {event}: ", exc_info=True)


# Cleanup quando o bot for desligado
def cleanup():
    """Limpa recursos ao desligar o bot.
    
    Responsável por:
    - Parar tarefas de monitoramento agendadas
    - Fechar conexão com banco de dados
    - Liberar recursos do sistema
    
    Chamado automaticamente no bloco finally do main.
    """
    try:
        scheduler.stop()  # Para as tasks de monitoramento
        db.close()
        logging.info("Recursos do bot liberados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao liberar recursos: {e}")


# --- INICIALIZAÇÃO DO BOT ---
if __name__ == "__main__":
    """Ponto de entrada principal do bot.
    
    Inicia o bot e garante que recursos sejam liberados
    corretamente mesmo em caso de erro ou interrupção.
    """
    try:
        logging.info("Iniciando NoobSquad Discord Bot...")
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        logging.info("Bot interrompido pelo usuário (Ctrl+C)")
    except Exception as e:
        logging.error(f"Erro ao iniciar o bot: {e}")
    finally:
        cleanup()
