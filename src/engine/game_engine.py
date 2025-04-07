import pygame
import esper
import json

from src.create.prefab_creator import create_bullet, create_enemy_spawner, create_input_player, create_player_square
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce_enemy import system_screen_bounce_enemy
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player


class GameEngine:
    def __init__(self) -> None:
        self._load_json()
        
        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode( (self.window_cfg["size"]["w"], 
                                                self.window_cfg["size"]["h"]), 
                                                pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"], 
                                     self.window_cfg["bg_color"]["g"], 
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()
        self.bullets_alive = 0


    def _load_json(self):
        with open("./assets/cfg/cfg_00/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("./assets/cfg/cfg_00/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("./assets/cfg/cfg_00/level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("./assets/cfg/cfg_00/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("./assets/cfg/cfg_00/bullet.json") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)


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
        self._player_entity = create_player_square(self.ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"])
        self._player_c_velocity = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_surface = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        
        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)


    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0 # self.clock.get_time() returns the time in milliseconds


    def _process_events(self):
        for events in pygame.event.get():
            system_input_player(self.ecs_world, events, self._do_action)
            if events.type == pygame.QUIT:
                self.is_running = False
            

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.delta_time, self.enemies_cfg)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce_enemy(self.ecs_world, self.screen)
        system_screen_player(self.ecs_world, self.screen)
        system_screen_bullet(self.ecs_world, self.screen)

        system_collision_player_enemy(self.ecs_world, self._player_entity, self.level_01_cfg)
        system_collision_bullet_enemy(self.ecs_world)
        self.ecs_world._clear_dead_entities()
        
        self.bullets_alive = len(self.ecs_world.get_component(CTagBullet)) # Lista de tuplas


    def _draw(self):
        self.screen.fill(self.bg_color)

        system_rendering(self.ecs_world, self.screen)

        pygame.display.flip()


    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()


    def _do_action(self, c_input:CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.vel.x += self.player_cfg["input_velocity"]
        elif c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.vel.x -= self.player_cfg["input_velocity"]
        elif c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.vel.y -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.vel.y += self.player_cfg["input_velocity"]
        elif c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.vel.y += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.vel.y -= self.player_cfg["input_velocity"]
        elif c_input.name == "PLAYER_FIRE":
            if c_input.phase == CommandPhase.START:
                if self.bullets_alive < self.level_01_cfg["player_spawn"]["max_bullets"]:
                    create_bullet(self.ecs_world, 
                                    c_input.mouse_pos, 
                                    self._player_c_transform.pos, 
                                    self.bullet_cfg, 
                                    self._player_c_surface.surf.get_size())
                