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
log_filename = datetime.now().strftime('bot_log_%Y-%m-%d.log')
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

if not DISCORD_TOKEN:
    logging.error("Token do bot não encontrado no arquivo .env")
    raise ValueError("Token do bot não encontrado no arquivo .env")

# --- CONFIGURAÇÃO DAS INTENTS E BOT ---
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents, heartbeat_timeout=60.0, help_command=None)

# Criar instância do scheduler
scheduler = MonitorScheduler(bot)


# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
def setup_database():
    """Inicializa a conexão com o banco de dados"""
    try:
        db.connect()
        db.initialize_collections()  # Inicializa as coleções e índices
        logging.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao inicializar banco de dados: {e}")
        raise e


# --- REGISTRAR OS COGS ---
async def setup_cogs():
    """Configura os Cogs do bot"""
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
    """Evento disparado quando o bot está pronto e conectado"""
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
    """Trata erros de comando."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"🤔 Comando não encontrado. Digite `!ajuda` para ver a lista de comandos disponíveis.")
    else:
        # Para outros erros, loga e informa o usuário
        logging.error(f"Ocorreu um erro no comando '{ctx.command}': {error}")
        await ctx.send("❌ Ocorreu um erro ao processar o comando. Por favor, tente novamente.")


@bot.event
async def on_error(event, *args, **kwargs):
    """Tratamento global de erros"""
    logging.error(f"Erro no evento {event}: ", exc_info=True)


# Cleanup quando o bot for desligado
def cleanup():
    """Limpa recursos ao desligar o bot"""
    try:
        scheduler.stop()  # Para as tasks de monitoramento
        db.close()
        logging.info("Recursos do bot liberados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao liberar recursos: {e}")


# Iniciar o bot
try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    logging.error(f"Erro ao iniciar o bot: {e}")
finally:
    cleanup()
