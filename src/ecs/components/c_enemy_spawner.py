

class CEnemySpawner:
    def __init__(self, spawn_events: list) -> None:
        # Cada evento debe contener: time, enemy_type, position, triggered
        self.spawn_events = [
            {**event, "triggered": False} for event in spawn_events
        ]
        self.elapsed_time = 0.0