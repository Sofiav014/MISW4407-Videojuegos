import esper

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet

def system_collision_bullet_enemy (ecs_world: esper.World, explosion_cfg: dict) -> None:
    """
    System to handle collision between bullet and enemies.
    This system checks for collisions between the bullet and enemy entities.
    If a collision is detected, the enemy entity is removed from the world.
    """
    
    enemy_components = ecs_world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = ecs_world.get_components(CSurface, CTransform, CTagBullet)
    
    for enemy_entity, (c_surface_e, c_transform_e, _) in enemy_components:
        enemy_rect = c_surface_e.area.copy()
        enemy_rect.topleft = c_transform_e.pos        
        for bullet_entity, (c_surface_b, c_transform_b, _) in bullet_components:
            bullet_rect = c_surface_b.area.copy()
            bullet_rect.topleft = c_transform_b.pos
            
            if enemy_rect.colliderect(bullet_rect):
                ecs_world.delete_entity(enemy_entity)
                ecs_world.delete_entity(bullet_entity)
                    
                
                if ecs_world.has_component(bullet_entity, CTagSpecialBullet):
                    create_explosion(ecs_world, c_transform_e.pos, explosion_cfg, 'special_image')
                    return True
                else:
                    create_explosion(ecs_world, c_transform_e.pos, explosion_cfg, 'normal_image')
    return False