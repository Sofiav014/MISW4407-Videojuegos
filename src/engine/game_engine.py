import pygame
import esper
import json

from src.create.prefab_creator import create_enemy_spawner
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce


class GameEngine:
    def __init__(self) -> None:
        
        self._load_json()
        pygame.init()

        pygame.display.set_caption(self.window_cfg["title"])

        self.screen = pygame.display.set_mode( (self.window_cfg["size"]["w"], 
                                                self.window_cfg["size"]["h"]), 
                                                pygame.SCALED)

        self.framerate = self.window_cfg["framerate"]

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.delta_time = 0


        self.ecs_world = esper.World()


    def _load_json(self):
        with open("./assets/cfg/cfg_00/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("./assets/cfg/cfg_00//enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("./assets/cfg/cfg_00//level_01.json") as level_01_file:
            self.level_cfg = json.load(level_01_file)


    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()


    def _create(self):
        create_enemy_spawner(self.ecs_world, self.level_cfg)


    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0 # self.clock.get_time() returns the time in milliseconds


    def _process_events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.is_running = False
            

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.delta_time, self.enemies_cfg)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)


    def _draw(self):
        self.screen.fill(
            (self.window_cfg["bg_color"]["r"], 
             self.window_cfg["bg_color"]["g"], 
             self.window_cfg["bg_color"]["b"])
        )

        system_rendering(self.ecs_world, self.screen)

        pygame.display.flip()


    def _clean(self):
        pygame.quit()
