"""
Utilitários Compartilhados entre Comandos

Este módulo contém:
- Validações compartilhadas (ex: validar canal de texto)
- Estruturas de dados globais para filas de música
- Estado compartilhado entre comandos

Autor: 1Kkayke
"""

import os
from typing import Dict
from collections import deque
from discord.ext import commands

def validar_canal(ctx: commands.Context) -> bool:
    """Valida se o comando foi enviado no canal de texto permitido.
    
    Verifica se o comando está sendo executado no canal configurado
    em CHAT_JUKEBOX. Isso previne spam em outros canais.
    
    Args:
        ctx: Contexto do comando Discord
    
    Returns:
        True se o canal é permitido, False caso contrário
    
    Example:
        >>> if not validar_canal(ctx):
        ...     await ctx.send("Use o canal correto!")
        ...     return
    """
    ALLOWED_CHANNEL_ID = int(os.getenv('CHAT_JUKEBOX', 0))
    if ALLOWED_CHANNEL_ID == 0:
        # Se não configurado, permite em qualquer canal
        return True
    return ctx.channel.id == ALLOWED_CHANNEL_ID

# --- Variáveis Globais Compartilhadas ---
# Estruturas de dados mantidas em memória durante execução do bot

# Fila de reprodução por servidor (guild_id -> deque de (url, preset))
play_queue: Dict[int, deque] = {}

# Informações da última música tocada por servidor (para autoplay e recomendações)
last_played_info: Dict[int, dict] = {}

# Estado do autoplay por servidor (guild_id -> bool)
autoplay_enabled: Dict[int, bool] = {}
