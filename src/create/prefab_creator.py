import pygame
import esper
import random

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def create_square(ecs_world:esper.World,
                   size:pygame.Vector2,
                   pos: pygame.Vector2,
                   vel: pygame.Vector2,
                   color: pygame.Color) -> int:

    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                            CTransform(pos))
    ecs_world.add_component(cuad_entity, 
                            CSurface(size,color))
    ecs_world.add_component(cuad_entity,
                            CVelocity(vel))
    return cuad_entity

def create_sprite(ecs_world:esper.World, pos:pygame.Vector2, vel: pygame.Vector2, surface:pygame.Surface) -> int:
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, 
                            CTransform(pos))
    ecs_world.add_component(sprite_entity, 
                            CVelocity(vel))
    ecs_world.add_component(sprite_entity, 
                            CSurface.from_surface(surface))
    return sprite_entity
    
    
def create_enemy_square(ecs_world:esper.World, pos:pygame.Vector2, enemy_info:dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    
    vel_x = random.uniform(vel_min, vel_max)
    vel_y = random.uniform(vel_min, vel_max)
    
    vel = pygame.Vector2(vel_x, vel_y)
    
    enemy_entity = create_sprite(ecs_world, pos, vel, enemy_surface)    
    ecs_world.add_component(enemy_entity, CTagEnemy())

def create_hunter_square(ecs_world:esper.World, pos:pygame.Vector2, hunter_info:dict):
    hunter_surface = ServiceLocator.images_service.get(hunter_info["image"])
    vel = pygame.Vector2(0, 0)
    enemy_entity = create_sprite(ecs_world, pos, vel, hunter_surface)
    ecs_world.add_component(enemy_entity, CAnimation(hunter_info["animations"]))
    ecs_world.add_component(enemy_entity, CHunterState(pos))
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ecs_world.add_component(enemy_entity, CTagHunter())


def create_player_square(ecs_world:esper.World, player_info:dict, player_lvl_info:dict) -> int:
    player_surface = ServiceLocator.images_service.get(player_info["image"])
    size = player_surface.get_size()
    size = pygame.Vector2(size[0] / player_info["animations"]["number_frames"], size[1])
    
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size.x / 2),
                         player_lvl_info["position"]["y"] - (size.y / 2))
    
    vel = pygame.Vector2(0,0)
    
    player_entity = create_sprite(ecs_world, pos, vel, player_surface)
    ecs_world.add_component(player_entity, CTagPlayer())
    ecs_world.add_component(player_entity, CAnimation(player_info["animations"]))
    ecs_world.add_component(player_entity, CPlayerState())
    return player_entity

def create_enemy_spawner(ecs_world:esper.World, level_cfg:dict) -> None:
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(spawner_entity, 
                            CEnemySpawner(level_cfg["enemy_spawn_events"]))


def create_input_player(ecs_world:esper.World) :
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_up = ecs_world.create_entity()
    input_down = ecs_world.create_entity()
    input_fire = ecs_world.create_entity()
    
    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    ecs_world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    ecs_world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    ecs_world.add_component(input_fire, CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))

def create_bullet(ecs_world:esper.World, end_pos:pygame.Vector2, start_pos:pygame.Vector2, bullet_info:dict, player_size:pygame.Vector2):
    """
    Creates a bullet entity in the ECS world with the specified properties.
    Args:
        ecs_world (esper.World): The ECS world where the bullet entity will be created.
        end_pos (pygame.Vector2): The target position indicating the direction of the bullet.
        start_pos (pygame.Vector2): The starting position of the bullet.
        bullet_info (dict): A dictionary containing bullet properties:
            - "size": A dictionary with "x" and "y" keys for the bullet's dimensions.
            - "color": A dictionary with "r", "g", and "b" keys for the bullet's color.
            - "velocity": A float representing the speed of the bullet.
        player_size (pygame.Vector2): The size of the player entity, used to calculate the bullet's initial position.
    Returns:
            None
    """
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    size = bullet_surface.get_rect().size
    pos = pygame.Vector2(start_pos.x + (player_size[0] / 2) - (size[0] / 2), 
                         start_pos.y + (player_size[1] / 2) - (size[1] / 2))
    direction = (end_pos - start_pos).normalize()
    vel = direction * bullet_info["velocity"]
    bullet_entity = create_sprite(ecs_world, pos, vel, bullet_surface)
    ecs_world.add_component(bullet_entity, CTagBullet())  


def create_explosion(world:esper.World, pos:pygame.Vector2, explosion_info:dict) -> int:
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    vel = pygame.Vector2(0, 0)
    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    world.add_component(explosion_entity, CTagExplosion())
    return explosion_entity