from dataclasses import dataclass

@dataclass
class Metrics:
    total_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0

metrics = Metrics()
