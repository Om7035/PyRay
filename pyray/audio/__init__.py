"""
PyRay Audio Module
Handles sound effects and music playback
"""

from pyray.audio.sound import (
    init_audio_device,
    close_audio_device,
    is_audio_device_ready,
    set_master_volume,
    
    # Sound functions
    load_sound,
    unload_sound,
    play_sound,
    stop_sound,
    pause_sound,
    resume_sound,
    is_sound_playing,
    set_sound_volume,
    set_sound_pitch,
    
    # Music functions
    load_music_stream,
    unload_music_stream,
    play_music_stream,
    stop_music_stream,
    pause_music_stream,
    resume_music_stream,
    is_music_stream_playing,
    set_music_volume,
    set_music_pitch,
    get_music_time_length,
    get_music_time_played,
    seek_music_stream,
    update_music_stream,
)

__all__ = [
    # Device management
    "init_audio_device",
    "close_audio_device",
    "is_audio_device_ready",
    "set_master_volume",
    
    # Sound
    "load_sound",
    "unload_sound",
    "play_sound",
    "stop_sound",
    "pause_sound",
    "resume_sound",
    "is_sound_playing",
    "set_sound_volume",
    "set_sound_pitch",
    
    # Music
    "load_music_stream",
    "unload_music_stream",
    "play_music_stream",
    "stop_music_stream",
    "pause_music_stream",
    "resume_music_stream",
    "is_music_stream_playing",
    "set_music_volume",
    "set_music_pitch",
    "get_music_time_length",
    "get_music_time_played",
    "seek_music_stream",
    "update_music_stream",
]
