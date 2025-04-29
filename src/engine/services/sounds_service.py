import pygame


class SoundsService:
    def __init__(self):
        self._sounds = {}
        

    def play (self, path: str, loop: bool = False):
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
            
        if loop:
            self._sounds[path].play(loops=-1)
        else:
            self._sounds[path].play()
    
    def stop (self, path: str):
        if path in self._sounds:
            self._sounds[path].stop()