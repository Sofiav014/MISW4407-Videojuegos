import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter import CTagHunter


def system_screen_bounce_enemy(world:esper.World, screen:pygame.Surface) -> None:
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CVelocity, CTagEnemy)

    c_transform: CTransform
    c_surface: CSurface
    c_velocity: CVelocity

    for entity, (c_transform, c_surface, c_velocity, _) in components:

        if (not(world.has_component(entity, CTagHunter))):

            cuad_rect = c_surface.surf.get_rect(topleft=c_transform.pos)
            if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
                c_velocity.vel.x *= -1
                cuad_rect.clamp_ip(screen_rect)
                c_transform.pos.x = cuad_rect.x

            if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
                c_velocity.vel.y *= -1
                cuad_rect.clamp_ip(screen_rect)
                c_transform.pos.y = cuad_rect.y

