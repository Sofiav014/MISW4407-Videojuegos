import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_screen_player(world:esper.World, screen:pygame.Surface) -> None:
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagPlayer)

    c_transform: CTransform
    c_surface: CSurface

    for _, (c_transform, c_surface, _) in components:
        player_rect = c_surface.surf.get_rect(topleft=c_transform.pos)

        if not screen_rect.contains(player_rect):
            player_rect.clamp_ip(screen_rect)
            c_transform.pos.x = player_rect.x
            c_transform.pos.y = player_rect.y

