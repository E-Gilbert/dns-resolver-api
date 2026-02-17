from pydantic import BaseModel, Field
from typing import Any, Dict, List

class ResolveResponse(BaseModel):
    domain: str
    record_type: str
    cached: bool
    latency_ms: int
    ttl_seconds: int
    answers: List[Dict[str, Any]] = Field(default_factory=list)

class MetricsResponse(BaseModel):
    total_queries: int
    cache_hits: int
    cache_misses: int
    cache_size: int
