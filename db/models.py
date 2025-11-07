"""
Modelos de Dados para o Bot

Este módulo define as estruturas de dados usadas pelo bot:
- Song: Representação de uma música no histórico
- MusicPreference: Preferências musicais do usuário
- MonitoredChannel: Canal monitorado (YouTube ou Twitch)
- UserProfile: Perfil completo do usuário

Todos os modelos usam dataclasses para simplificação e 
incluem métodos para conversão para/de dicionários MongoDB.

Autor: 1Kkayke
"""

from datetime import datetime, UTC
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Representa uma música no histórico de reprodução.
    
    Attributes:
        title: Título da música
        url: URL do YouTube
        played_at: Data/hora em que foi tocada
        artist: Nome do artista (opcional)
        genre: Gênero musical (opcional)
    """
    title: str
    url: str
    played_at: datetime
    artist: Optional[str] = None
    genre: Optional[str] = None


@dataclass
class MusicPreference:
    """Representa uma preferência musical do usuário.
    
    Usado para rastrear gostos musicais e gerar recomendações.
    
    Attributes:
        name: Nome do gênero, artista ou banda
        type: Tipo da preferência ('genre', 'artist', 'band')
        count: Número de vezes que músicas deste tipo foram tocadas
        last_updated: Data/hora da última atualização
    """
    name: str  # Nome do gênero, artista ou banda
    type: str  # 'genre', 'artist', 'band'
    count: int  # Número de vezes que músicas deste tipo foram tocadas
    last_updated: datetime


@dataclass
class MonitoredChannel:
    """Representa um canal monitorado (YouTube ou Twitch).
    
    Armazenado em coleção separada no MongoDB com sistema de assinaturas.
    Múltiplos usuários podem se inscrever no mesmo canal.
    
    Attributes:
        platform: 'youtube' ou 'twitch'
        channel_id: ID único do canal na plataforma
        channel_name: Nome de exibição do canal
        added_by: Discord user ID de quem adicionou primeiro (opcional)
        last_video_id: ID do último vídeo postado (YouTube)
        last_stream_id: ID da última stream (Twitch)
        is_live: Status atual de transmissão ao vivo
        added_at: Data/hora de quando foi adicionado
        subscribers: Lista de Discord user IDs inscritos
    """
    platform: str  # 'youtube' ou 'twitch'
    channel_id: str
    channel_name: str
    added_by: Optional[str] = None  # Discord user ID who first added the channel
    last_video_id: Optional[str] = None
    last_stream_id: Optional[str] = None
    is_live: bool = False
    added_at: datetime = datetime.now(UTC)  # Usando UTC de forma explícita
    subscribers: Optional[List[str]] = None

    def __post_init__(self):
        if self.subscribers is None:
            self.subscribers = []

    @classmethod
    def from_dict(cls, data: Dict) -> 'MonitoredChannel':
        return cls(
            platform=data.get('platform'),
            channel_id=data.get('channel_id'),
            channel_name=data.get('channel_name'),
            added_by=data.get('added_by'),
            last_video_id=data.get('last_video_id'),
            last_stream_id=data.get('last_stream_id'),
            is_live=data.get('is_live', False),
            added_at=data.get('added_at', datetime.now(UTC)),
            subscribers=data.get('subscribers', [])
        )

    def to_dict(self) -> Dict:
        return {
            'platform': self.platform,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'added_by': self.added_by,
            'last_video_id': self.last_video_id,
            'last_stream_id': self.last_stream_id,
            'is_live': self.is_live,
            'added_at': self.added_at,
            'subscribers': self.subscribers or []
        }


@dataclass
class UserProfile:
    """Representa o perfil completo de um usuário no MongoDB.
    
    Contém todo o histórico musical, preferências e estatísticas.
    
    Attributes:
        discord_id: ID único do usuário no Discord (string)
        username: Nome de usuário no Discord
        music_history: Lista de músicas tocadas (máximo 100 recentes)
        music_preferences: Lista de preferências musicais
        created_at: Data/hora de criação do perfil
    """
    discord_id: str
    username: str
    music_history: List[Song] = None  # Será inicializado como lista vazia
    music_preferences: List[MusicPreference] = None  # Será inicializado como lista vazia
    created_at: datetime = None  # Será inicializado com datetime.now(UTC)

    def __post_init__(self):
        """Inicializa campos com valores padrão se necessário"""
        if self.music_history is None:
            self.music_history = []
        if self.music_preferences is None:
            self.music_preferences = []
        if self.created_at is None:
            self.created_at = datetime.now(UTC)

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Cria um UserProfile a partir de um dicionário do MongoDB"""
        return cls(
            discord_id=data['discord_id'],
            username=data['username'],
            music_history=[
                Song(
                    title=song['title'],
                    url=song['url'],
                    played_at=song['played_at'],
                    artist=song.get('artist'),
                    genre=song.get('genre')
                ) for song in data.get('music_history', [])
            ],
            music_preferences=[
                MusicPreference(
                    name=pref['name'],
                    type=pref['type'],
                    count=pref['count'],
                    last_updated=pref['last_updated']
                ) for pref in data.get('music_preferences', [])
            ],
            created_at=data.get('created_at')
        )

    def to_dict(self) -> Dict:
        """Converte o UserProfile para um dicionário para salvar no MongoDB"""
        return {
            'discord_id': self.discord_id,
            'username': self.username,
            'music_history': [
                {
                    'title': song.title,
                    'url': song.url,
                    'played_at': song.played_at,
                    'artist': song.artist,
                    'genre': song.genre
                } for song in self.music_history
            ],
            'music_preferences': [
                {
                    'name': pref.name,
                    'type': pref.type,
                    'count': pref.count,
                    'last_updated': pref.last_updated
                } for pref in self.music_preferences
            ],
            'created_at': self.created_at
        }


__all__ = ['Song', 'MusicPreference', 'MonitoredChannel', 'UserProfile']
