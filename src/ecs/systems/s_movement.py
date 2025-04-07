import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_movement(world:esper.World, delta_time:float) -> None:
    components = world.get_components(CVelocity, CTransform)

    c_velocity: CSurface
    c_transform: CTransform

    for _, (c_velocity, c_transform) in components:
        c_transform.pos.x += c_velocity.vel.x * delta_time
        c_transform.pos.y += c_velocity.vel.y * delta_time
        

