import pygame

class TextsService:
    def __init__(self) -> None:
        self._texts = {}

    def get(self, path:str, size: int) -> pygame.font.Font:
        if path not in self._texts:
            self._texts[(path,size)] = pygame.font.Font(path,size)
        return self._texts[(path,size)]