import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet

def system_special_bullet_lockon(world:esper.World) -> int:
    enemy_distance = {}
    enemy_components = world.get_components(CTransform, CTagEnemy)
    bullet_components = world.get_components(CTransform, CTagSpecialBullet)
    for _, (c_transform, _) in bullet_components:
        for enemy_entity, (c_enemy_transform, _) in enemy_components:
            enemy_distance[enemy_entity] = c_transform.pos.distance_to(c_enemy_transform.pos)
            
    if(len(enemy_distance) > 0):
        enemy = min(enemy_distance, key=enemy_distance.get)
        return enemy
    return None
    
    
    