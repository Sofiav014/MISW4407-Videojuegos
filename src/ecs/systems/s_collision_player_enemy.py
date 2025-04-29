import esper

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_player_enemy (ecs_world: esper.World, player_entity: int, level_cfg: dict, explosion_cfg: dict) -> None:
    """
    System to handle collision between player and enemies.
    This system checks for collisions between the player and enemy entities.
    If a collision is detected, the enemy entity is removed from the world.
    """
    
    components = ecs_world.get_components(CSurface, CTransform, CTagEnemy)
    
    pl_t : CTransform = ecs_world.component_for_entity(player_entity, CTransform)
    pl_s : CSurface = ecs_world.component_for_entity(player_entity, CSurface)
    
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    
    for enemy_entity, (c_surface, c_transform, _) in components:
        enemy_rect = CSurface.get_area_relative(c_surface.area, c_transform.pos)

        if pl_rect.colliderect(enemy_rect):
            ecs_world.delete_entity(enemy_entity)

            
            #Devolver el player a su posicion inicial
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - (pl_s.surf.get_width() / 2)
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - (pl_s.surf.get_height() / 2)

            create_explosion(ecs_world, c_transform.pos, explosion_cfg, 'normal_image')