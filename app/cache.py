import time
from typing import Any, Dict, Optional, Tuple
from .config import CACHE_DEFAULT_TTL_SECONDS, MAX_ITEMS_IN_CACHE

_store: Dict[str, Tuple[float, int, Any]] = {}

def _now() -> float:
    return time.time()

def get(key: str) -> Optional[Tuple[int, Any]]:
    item = _store.get(key)
    if not item:
        return None
    expires_at, ttl, value = item
    if _now() >= expires_at:
        _store.pop(key, None)
        return None
    return ttl, value

def set(key: str, value: Any, ttl: int = CACHE_DEFAULT_TTL_SECONDS) -> None:
    if len(_store) >= MAX_ITEMS_IN_CACHE:
        expired = [k for k, (exp, _, _) in _store.items() if _now() >= exp]
        for k in expired[:500]:
            _store.pop(k, None)
        if len(_store) >= MAX_ITEMS_IN_CACHE:
            _store.pop(next(iter(_store)), None)

    expires_at = _now() + max(1, ttl)
    _store[key] = (expires_at, ttl, value)

def size() -> int:
    expired = [k for k, (exp, _, _) in _store.items() if _now() >= exp]
    for k in expired[:500]:
        _store.pop(k, None)
    return len(_store)
