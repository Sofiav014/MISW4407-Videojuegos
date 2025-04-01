import pygame
import esper
import random

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_spawner import CEnemySpawner

def create_square(ecs_world:esper.World,
                   size:pygame.Vector2,
                   pos: pygame.Vector2,
                   vel: pygame.Vector2,
                   color: pygame.Color) -> None:

    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                            CTransform(pos))
    ecs_world.add_component(cuad_entity, 
                            CSurface(size,color))
    ecs_world.add_component(cuad_entity,
                            CVelocity(vel))
    
    
def create_enemy_square(ecs_world:esper.World, pos:pygame.Vector2, enemy_info:dict):
    size = pygame.Vector2(enemy_info["size"]["x"], 
                          enemy_info["size"]["y"])
    
    color = pygame.Color(enemy_info["color"]["r"],
                       enemy_info["color"]["g"],
                       enemy_info["color"]["b"])
    
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    
    vel_x = random.uniform(vel_min, vel_max)
    vel_y = random.uniform(vel_min, vel_max)
    
    vel = pygame.Vector2(vel_x, vel_y)
    
    create_square(ecs_world, size, pos, vel, color)    


def create_player_square(ecs_world:esper.World, player_info:dict, player_lvl_info:dict) -> None:
    size = pygame.Vector2(player_info["size"]["x"], 
                          player_info["size"]["y"])
    
    color = pygame.Color(player_info["color"]["r"],
                       player_info["color"]["g"],
                       player_info["color"]["b"])
    
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - size.x / 2,
                         player_lvl_info["position"]["y"] - size.y / 2)
    
    vel = pygame.Vector2(0,0)
    
    create_square(ecs_world, size, pos, vel, color) 

def create_enemy_spawner(ecs_world:esper.World, level_cfg:dict) -> None:
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(spawner_entity, 
                            CEnemySpawner(level_cfg["enemy_spawn_events"]))
    