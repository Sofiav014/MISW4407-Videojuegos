import esper
import pygame
import random

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

                size = pygame.Vector2(config["size"]["x"], config["size"]["y"])
                pos = pygame.Vector2(event["position"]["x"], event["position"]["y"])
                
                vel_x = random.uniform(config["velocity_min"], config["velocity_max"])
                vel_y = random.uniform(config["velocity_min"], config["velocity_max"])
                vel = pygame.Vector2(vel_x, vel_y)

                color = pygame.Color(config["color"]["r"], config["color"]["g"], config["color"]["b"])

                create_enemy_cuadrado(world, pos, config)
                event["triggered"] = True

                print(f"[ENEMY SPAWNED] Type: {enemy_type} | "
                      f"Position: ({pos.x:.1f}, {pos.y:.1f}) | "
                      f"Size: ({size.x}, {size.y}) | "
                      f"Color: ({color.r}, {color.g}, {color.b}) | "
                      f"Velocity: ({vel.x:.2f}, {vel.y:.2f}) | "
                      f"Time: {c_enemy_spawner.elapsed_time:.2f}s")
        
        
        
    