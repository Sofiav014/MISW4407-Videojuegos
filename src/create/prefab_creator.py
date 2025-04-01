import pygame
import esper

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform

def crear_cuadrado(ecs_world:esper.World,
                   size:pygame.Vector2,
                   pos: pygame.Vector2,
                   vel: pygame.Vector2,
                   col: pygame.Color) -> None:

    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity, 
                            CSurface(size,col))
    ecs_world.add_component(cuad_entity,
                            CTransform(pos))
    ecs_world.add_component(cuad_entity,
                            CVelocity(vel))