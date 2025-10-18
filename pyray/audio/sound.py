"""
Sound and music module for PyRay
Handles audio playback and management
"""

import pygame
from typing import Optional, Dict
from pyray.core.config import Config


class Sound:
    """Represents a loaded sound effect"""
    
    def __init__(self, pygame_sound: pygame.mixer.Sound, filename: str):
        self.sound = pygame_sound
        self.filename = filename
        self.channel: Optional[pygame.mixer.Channel] = None
        self.volume = 1.0
        self.pitch = 1.0
        
    def play(self) -> None:
        """Play the sound"""
        self.channel = self.sound.play()
        if self.channel:
            self.channel.set_volume(self.volume)
            
    def stop(self) -> None:
        """Stop the sound"""
        if self.channel:
            self.channel.stop()
            
    def pause(self) -> None:
        """Pause the sound"""
        if self.channel:
            self.channel.pause()
            
    def resume(self) -> None:
        """Resume the sound"""
        if self.channel:
            self.channel.unpause()
            
    def is_playing(self) -> bool:
        """Check if sound is playing"""
        if self.channel:
            return self.channel.get_busy()
        return False
        
    def set_volume(self, volume: float) -> None:
        """Set sound volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        self.sound.set_volume(self.volume)
        
    def set_pitch(self, pitch: float) -> None:
        """Set sound pitch (not directly supported in pygame)"""
        self.pitch = pitch
        # Note: Pygame doesn't support pitch shifting directly
        # This would require additional audio processing library


class Music:
    """Represents a music stream"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.volume = 1.0
        self.pitch = 1.0
        self.loaded = False
        
        try:
            pygame.mixer.music.load(filename)
            self.loaded = True
        except Exception as e:
            print(f"Error loading music {filename}: {e}")
            
    def play(self, loops: int = -1) -> None:
        """Play the music stream"""
        if self.loaded:
            pygame.mixer.music.play(loops)
            pygame.mixer.music.set_volume(self.volume)
            
    def stop(self) -> None:
        """Stop the music stream"""
        pygame.mixer.music.stop()
        
    def pause(self) -> None:
        """Pause the music stream"""
        pygame.mixer.music.pause()
        
    def resume(self) -> None:
        """Resume the music stream"""
        pygame.mixer.music.unpause()
        
    def is_playing(self) -> bool:
        """Check if music is playing"""
        return pygame.mixer.music.get_busy()
        
    def set_volume(self, volume: float) -> None:
        """Set music volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        
    def set_pitch(self, pitch: float) -> None:
        """Set music pitch (not directly supported in pygame)"""
        self.pitch = pitch
        
    def get_time_length(self) -> float:
        """Get music time length in seconds"""
        # Not directly supported in pygame
        return 0.0
        
    def get_time_played(self) -> float:
        """Get current music time played in seconds"""
        return pygame.mixer.music.get_pos() / 1000.0 if self.loaded else 0.0
        
    def seek(self, position: float) -> None:
        """Seek to position in seconds"""
        if self.loaded:
            pygame.mixer.music.set_pos(position)


class AudioManager:
    """Manages audio system and resources"""
    
    def __init__(self):
        self.initialized = False
        self.master_volume = 1.0
        self.sounds: Dict[str, Sound] = {}
        self.current_music: Optional[Music] = None
        
    def init(self, frequency: int = 22050, size: int = -16, 
             channels: int = 2, buffer: int = 512) -> None:
        """Initialize audio device"""
        try:
            pygame.mixer.init(frequency, size, channels, buffer)
            self.initialized = True
            Config.instance().audio_initialized = True
        except Exception as e:
            print(f"Error initializing audio device: {e}")
            self.initialized = False
            
    def close(self) -> None:
        """Close audio device"""
        if self.initialized:
            pygame.mixer.quit()
            self.initialized = False
            Config.instance().audio_initialized = False
            
    def is_ready(self) -> bool:
        """Check if audio device is ready"""
        return self.initialized
        
    def set_master_volume(self, volume: float) -> None:
        """Set master volume for all sounds"""
        self.master_volume = max(0.0, min(1.0, volume))
        # This would affect all new sounds played
        
    def load_sound(self, filename: str) -> Sound:
        """Load sound from file"""
        if filename in self.sounds:
            return self.sounds[filename]
            
        try:
            pygame_sound = pygame.mixer.Sound(filename)
            sound = Sound(pygame_sound, filename)
            self.sounds[filename] = sound
            return sound
        except Exception as e:
            print(f"Error loading sound {filename}: {e}")
            # Return a dummy sound
            dummy_sound = pygame.mixer.Sound(buffer=bytes(100))
            return Sound(dummy_sound, filename)
            
    def unload_sound(self, sound: Sound) -> None:
        """Unload sound from memory"""
        if sound.filename in self.sounds:
            del self.sounds[sound.filename]
            
    def load_music(self, filename: str) -> Music:
        """Load music stream from file"""
        music = Music(filename)
        self.current_music = music
        return music
        
    def unload_music(self, music: Music) -> None:
        """Unload music stream"""
        if self.current_music == music:
            music.stop()
            self.current_music = None


# Global audio manager
_audio_manager = AudioManager()


# Public API functions
def init_audio_device() -> None:
    """Initialize audio device and context"""
    _audio_manager.init()


def close_audio_device() -> None:
    """Close the audio device and context"""
    _audio_manager.close()


def is_audio_device_ready() -> bool:
    """Check if audio device has been initialized successfully"""
    return _audio_manager.is_ready()


def set_master_volume(volume: float) -> None:
    """Set master volume (0.0 to 1.0)"""
    _audio_manager.set_master_volume(volume)


# Sound functions
def load_sound(filename: str) -> Sound:
    """Load sound from file"""
    return _audio_manager.load_sound(filename)


def unload_sound(sound: Sound) -> None:
    """Unload sound"""
    _audio_manager.unload_sound(sound)


def play_sound(sound: Sound) -> None:
    """Play a sound"""
    sound.play()


def stop_sound(sound: Sound) -> None:
    """Stop playing a sound"""
    sound.stop()


def pause_sound(sound: Sound) -> None:
    """Pause a sound"""
    sound.pause()


def resume_sound(sound: Sound) -> None:
    """Resume a paused sound"""
    sound.resume()


def is_sound_playing(sound: Sound) -> bool:
    """Check if a sound is currently playing"""
    return sound.is_playing()


def set_sound_volume(sound: Sound, volume: float) -> None:
    """Set volume for a sound (0.0 to 1.0)"""
    sound.set_volume(volume)


def set_sound_pitch(sound: Sound, pitch: float) -> None:
    """Set pitch for a sound"""
    sound.set_pitch(pitch)


# Music functions
def load_music_stream(filename: str) -> Music:
    """Load music stream from file"""
    return _audio_manager.load_music(filename)


def unload_music_stream(music: Music) -> None:
    """Unload music stream"""
    _audio_manager.unload_music(music)


def play_music_stream(music: Music) -> None:
    """Start music playing"""
    music.play()


def stop_music_stream(music: Music) -> None:
    """Stop music playing"""
    music.stop()


def pause_music_stream(music: Music) -> None:
    """Pause music playing"""
    music.pause()


def resume_music_stream(music: Music) -> None:
    """Resume playing paused music"""
    music.resume()


def is_music_stream_playing(music: Music) -> bool:
    """Check if music is playing"""
    return music.is_playing()


def set_music_volume(music: Music, volume: float) -> None:
    """Set volume for music (0.0 to 1.0)"""
    music.set_volume(volume)


def set_music_pitch(music: Music, pitch: float) -> None:
    """Set pitch for music"""
    music.set_pitch(pitch)


def get_music_time_length(music: Music) -> float:
    """Get music time length in seconds"""
    return music.get_time_length()


def get_music_time_played(music: Music) -> float:
    """Get current music time played in seconds"""
    return music.get_time_played()


def seek_music_stream(music: Music, position: float) -> None:
    """Seek music to a position (in seconds)"""
    music.seek(position)


def update_music_stream(music: Music) -> None:
    """Updates buffers for music streaming (not needed in pygame)"""
    pass  # pygame handles this automatically
