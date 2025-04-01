import esper
import pygame
import random

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.create.prefab_creator import crear_cuadrado

def system_enemy_spawner(world: esper.World, 
                         delta_time: float, 
                         enemy_data: dict) -> None:
    spawner_entity = next((e for e, c in world.get_component(CEnemySpawner)), None)
    if spawner_entity is None:
        return
    
    spawner = world.component_for_entity(spawner_entity, CEnemySpawner)
    spawner.elapsed_time += delta_time

    for event in spawner.spawn_events:
        if not event["triggered"] and spawner.elapsed_time >= event["time"]:
            enemy_type = event["enemy_type"]
            config = enemy_data[enemy_type]

            size = pygame.Vector2(config["size"]["x"], config["size"]["y"])
            pos = pygame.Vector2(event["position"]["x"], event["position"]["y"])
            
            # Dirección aleatoria
            angle = random.uniform(0, 360)
            speed = random.uniform(config["velocity_min"], config["velocity_max"])
            vel = pygame.Vector2(speed, 0).rotate(angle)

            color = pygame.Color(config["color"]["r"], config["color"]["g"], config["color"]["b"])

            crear_cuadrado(world, size, pos, vel, color)
            event["triggered"] = True
