import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_special_text import CSpecialText
from src.engine.service_locator import ServiceLocator

def system_special_bullet_charged(world:esper.World, deltatime:float, interface_info:dict):
    components = world.get_components(CSpecialText, CSurface)
    for _, (c_special_text, c_surface) in components:
        if not c_special_text.charged or not c_special_text.next:
            color = pygame.Color(255, 0, 0)
            c_special_text.curr_charge_time += deltatime
            if c_special_text.curr_charge_time > c_special_text.charge_time:
                c_special_text.curr_charge_time = c_special_text.charge_time
                c_special_text.charged = True            
        else:
            color = pygame.Color(0, 255, 0)

        font = ServiceLocator.texts_service.get(interface_info["font"], 
                                                interface_info["special"]["size"])
        text = str(round((c_special_text.curr_charge_time / c_special_text.charge_time)* 100) ) + "%"
        c_surface.surf = font.render(text, True, color)
        c_surface.area = c_surface.surf.get_rect()