import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def system_hunter_state(world:esper.World, player_entity: int, hunter_info: dict):
    c_transform_p = world.component_for_entity(player_entity, CTransform)

    components = world.get_components(CAnimation, CHunterState, CVelocity, CTransform)
    for _, (c_animation,c_state_h,c_velocity, c_transform) in components:
        if c_state_h.state == HunterState.IDLE:
            _do_idle_state(c_animation,c_state_h, c_velocity, c_transform, c_transform_p, hunter_info)
        elif c_state_h.state == HunterState.CHASE:
            _do_chase_state(c_animation,c_state_h, c_velocity, c_transform, c_transform_p, hunter_info)
        elif c_state_h.state == HunterState.RETURN:
            _do_return_state(c_animation,c_state_h, c_velocity, c_transform, c_transform_p, hunter_info)


def _do_idle_state(c_animation:CAnimation, c_state_h:CHunterState, c_velocity:CVelocity, 
                   c_transform:CTransform, c_transform_p:CTransform, hunter_info:dict):
    _set_animation(c_animation, 1)
    c_velocity.vel.x = 0
    c_velocity.vel.y = 0

    dist = c_transform.pos.distance_to(c_transform_p.pos)
    if dist < hunter_info["distance_start_chase"]:
        ServiceLocator.sounds_service.play(hunter_info["sound_chase"])
        c_state_h.state = HunterState.CHASE

def _do_chase_state(c_animation:CAnimation, c_state_h:CHunterState, c_velocity:CVelocity,
                    c_transform:CTransform, c_transform_p:CTransform, hunter_info:dict):
    _set_animation(c_animation, 0)
    c_velocity.vel = (c_transform_p.pos - c_transform.pos).normalize() * hunter_info["velocity_chase"]
    dist = c_state_h.start_pos.distance_to(c_transform.pos)
    if dist >= hunter_info["distance_start_return"]:
        c_state_h.state = HunterState.RETURN


def _do_return_state(c_animation:CAnimation, c_state_h:CHunterState, c_velocity:CVelocity,
                     c_transform:CTransform, c_transform_p:CTransform, hunter_info:dict):
    _set_animation(c_animation, 0)
    c_velocity.vel = (c_state_h.start_pos - c_transform.pos).normalize() * hunter_info["velocity_return"]
    dist = c_state_h.start_pos.distance_to(c_transform.pos)
    if dist <= 2:
        c_transform.pos.xy = c_state_h.start_pos.xy
        c_state_h.state = HunterState.IDLE

def _set_animation(c_animation:CAnimation, num_anim:int):
    if c_animation.current_animation != num_anim:
        c_animation.current_animation = num_anim
        c_animation.current_animation_time = 0
        c_animation.curr_frame = c_animation.animations_list[c_animation.current_animation].start