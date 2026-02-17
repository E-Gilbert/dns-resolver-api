from fastapi import FastAPI, Query, HTTPException
from .schemas import ResolveResponse, MetricsResponse
from .dns_client import resolve as dns_resolve, SUPPORTED_TYPES
from .cache import get as cache_get, set as cache_set, size as cache_size
from .metrics import metrics

app = FastAPI(title="DNS Resolver API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/resolve", response_model=ResolveResponse)
def resolve(
    domain: str = Query(..., min_length=1, description="Domain name, e.g. example.com"),
    record_type: str = Query("A", description=f"One of: {', '.join(sorted(SUPPORTED_TYPES))}")
):
    metrics.total_queries += 1
    key = f"{domain.lower().strip()}::{record_type.upper().strip()}"

    cached = cache_get(key)
    if cached:
        metrics.cache_hits += 1
        ttl, answers = cached
        return ResolveResponse(
            domain=domain,
            record_type=record_type.upper(),
            cached=True,
            latency_ms=0,
            ttl_seconds=ttl,
            answers=answers
        )

    metrics.cache_misses += 1

    try:
        latency_ms, answers, ttl = dns_resolve(domain, record_type)

        ttl_to_store = max(10, min(int(ttl), 3600))
        cache_set(key, answers, ttl=ttl_to_store)

        return ResolveResponse(
            domain=domain,
            record_type=record_type.upper(),
            cached=False,
            latency_ms=latency_ms,
            ttl_seconds=ttl_to_store,
            answers=answers
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    return MetricsResponse(
        total_queries=metrics.total_queries,
        cache_hits=metrics.cache_hits,
        cache_misses=metrics.cache_misses,
        cache_size=cache_size()
    )
