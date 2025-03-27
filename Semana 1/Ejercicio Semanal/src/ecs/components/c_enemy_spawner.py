

class CEnemySpawner:
    def __init__(self, spawn_data: dict) -> None:
        spawn_events = spawn_data["enemy_spawn_events"]        
        self.spawn_events = [
            {**event, "triggered": False} for event in spawn_events
        ]
        self.elapsed_time = 0.0