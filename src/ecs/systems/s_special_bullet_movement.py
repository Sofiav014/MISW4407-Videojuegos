import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet

def system_special_bullet_movement(world:esper.World, lockon_entity: int, special_info:dict):

    if(lockon_entity != None):
        lockon_c_transform = world.component_for_entity(lockon_entity, CTransform)
        components = world.get_components(CVelocity, CTransform, CTagSpecialBullet)
        for _, (c_velocity, c_transform, _) in components:
            c_velocity.vel = (lockon_c_transform.pos - c_transform.pos).normalize() * special_info["velocity"]