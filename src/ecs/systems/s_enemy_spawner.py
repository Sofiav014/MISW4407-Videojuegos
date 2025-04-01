import esper
import pygame


from src.ecs.components.c_enemy_spawner import CEnemySpawner, SpawnEventData
from src.create.prefab_creator import create_enemy_cuadrado


def system_enemy_spawner(world: esper.World, 
                         delta_time: float, 
                         enemy_data: dict) -> None:
    
    components = world.get_component(CEnemySpawner)
    
    c_enemy_spawner: CEnemySpawner
    
    for _, c_enemy_spawner in components:
        c_enemy_spawner.elapsed_time += delta_time
        spw_event:SpawnEventData
        for spw_event in c_enemy_spawner.spawn_event_data:
            if not spw_event.triggered and c_enemy_spawner.elapsed_time >= spw_event.time: 
                spw_event.triggered = True                
                
                create_enemy_cuadrado(world, 
                                      spw_event.position,
                                      enemy_data[spw_event.enemy_type])

        
        
        
    