import pygame
import os
import sys
import random
import glob
import threading

class SoundManager:
    def __init__(self, pack_name='mxblue', volume=1.0):
        self.pack_name = pack_name
        self.volume = volume
        self.sounds = {
            'press': {},
            'release': {}
        }
        self.lock = threading.RLock() # Re-entrant lock for thread safety
        
        # Initialize pygame mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        # Set a reasonable number of channels to allow multiple overlapping sounds
        pygame.mixer.set_num_channels(32)
        
        self.load_sounds()

    def get_available_packs(self):
        """Returns a list of available sound packs in the sounds directory."""
        sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
    def get_resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)

    def get_available_packs(self):
        """Returns a list of available sound packs in the sounds directory."""
        sounds_dir = self.get_resource_path('sounds')
        if not os.path.exists(sounds_dir):
            return []
        try:
            packs = [d for d in os.listdir(sounds_dir) if os.path.isdir(os.path.join(sounds_dir, d))]
            return sorted(packs)
        except OSError:
            return []

    def set_pack(self, pack_name):
        """Switches the sound pack safely."""
        with self.lock:
            if pack_name == self.pack_name:
                return
            self.pack_name = pack_name
            self.sounds['press'].clear()
            self.sounds['release'].clear()
            self.load_sounds()

    def set_volume(self, volume):
        """Sets the volume (0.0 to 1.0)."""
        with self.lock:
            self.volume = max(0.0, min(1.0, volume))
            # Update existing sounds
            for sound_type in self.sounds:
                for sound in self.sounds[sound_type].values():
                    sound.set_volume(self.volume)

    def load_sounds(self):
        """Loads all sound files into memory."""
        # lock is held by caller (set_pack or __init__) if strictly following pattern,
        # but to be safe, we can assume this is internal. 
        # Ideally, we allow re-entrant lock.
        
        
        base_path = self.get_resource_path(os.path.join('sounds', self.pack_name))
        
        
        load_errors = []

        # Load press sounds
        press_path = os.path.join(base_path, 'press')
        if os.path.exists(press_path):
            for file in os.listdir(press_path):
                if file.endswith('.mp3'):
                    key_name = os.path.splitext(file)[0]
                    full_path = os.path.join(press_path, file)
                    try:
                        sound = pygame.mixer.Sound(full_path)
                        sound.set_volume(self.volume)
                        self.sounds['press'][key_name] = sound
                    except pygame.error as e:
                        load_errors.append(f"press/{file}: {e}")

        # Load release sounds
        release_path = os.path.join(base_path, 'release')
        if os.path.exists(release_path):
            for file in os.listdir(release_path):
                if file.endswith('.mp3'):
                    key_name = os.path.splitext(file)[0]
                    full_path = os.path.join(release_path, file)
                    try:
                        sound = pygame.mixer.Sound(full_path)
                        sound.set_volume(self.volume)
                        self.sounds['release'][key_name] = sound
                    except pygame.error as e:
                        load_errors.append(f"release/{file}: {e}")
        
        if load_errors:
            print(f"Warnings loading pack '{self.pack_name}': {', '.join(load_errors)}")
        print(f"Loaded {len(self.sounds['press'])} press sounds and {len(self.sounds['release'])} release sounds for '{self.pack_name}'.")

    def play_sound(self, key_code, event_type='press'):
        """
        Plays a sound for the given key code and event type.
        Thread-safe.
        """
        with self.lock:
            if event_type not in self.sounds:
                return

            sound_map = self.sounds[event_type]
            sound_to_play = None
            
            # Normalize key
            # pynput Key objects need to be converted to strings matching our files
            normalized_key = str(key_code).replace('Key.', '').upper()
            if hasattr(key_code, 'char') and key_code.char:
                 # Handle characters somewhat if we had specific char sounds
                 pass

            if normalized_key in sound_map:
                 sound_to_play = sound_map[normalized_key]
            
            elif event_type == 'press':
                 generics = [k for k in sound_map.keys() if k.startswith('GENERIC_R')]
                 if generics:
                     random_key = random.choice(generics)
                     sound_to_play = sound_map[random_key]
                 # Fallback if no generics found (e.g. pack only has specific keys? Unlikely for kbsim packs)
                 elif sound_map:
                     sound_to_play = random.choice(list(sound_map.values()))
                     
            elif event_type == 'release':
                if 'GENERIC' in sound_map:
                    sound_to_play = sound_map['GENERIC']
                elif sound_map:
                    sound_to_play = random.choice(list(sound_map.values()))
            
            if sound_to_play:
                sound_to_play.play()
