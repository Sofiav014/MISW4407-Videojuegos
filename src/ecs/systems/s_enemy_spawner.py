import esper
import pygame


from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.create.prefab_creator import create_enemy_cuadrado


def system_enemy_spawner(world: esper.World, 
                         delta_time: float, 
                         enemy_data: dict) -> None:
    
    components = world.get_component(CEnemySpawner)
    
    c_enemy_spawner: CEnemySpawner
    
    for entity, c_enemy_spawner in components:
        c_enemy_spawner.elapsed_time += delta_time
        
        for event in c_enemy_spawner.spawn_events:
            if not event["triggered"] and c_enemy_spawner.elapsed_time >= event["time"]:
                
                enemy_type = event["enemy_type"]
                config = enemy_data[enemy_type]
                pos = pygame.Vector2(event["position"]["x"], event["position"]["y"])
            
                create_enemy_cuadrado(world, pos, config)
                event["triggered"] = True

        
        
        
    