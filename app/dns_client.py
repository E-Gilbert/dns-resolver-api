import time
from typing import Any, Dict, List, Tuple
import dns.resolver
import dns.exception

from .config import DNS_TIMEOUT_SECONDS, CACHE_DEFAULT_TTL_SECONDS

SUPPORTED_TYPES = {"A", "AAAA", "MX", "TXT", "CNAME", "NS"}

def resolve(domain: str, record_type: str) -> Tuple[int, List[Dict[str, Any]], int]:
    record_type = record_type.upper().strip()
    if record_type not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported record type: {record_type}")

    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["8.8.8.8", "8.8.4.4"]
    resolver.lifetime = DNS_TIMEOUT_SECONDS
    resolver.timeout = DNS_TIMEOUT_SECONDS

    start = time.perf_counter()
    try:
        answer = resolver.resolve(domain, record_type)
        latency_ms = int((time.perf_counter() - start) * 1000)

        ttl = getattr(answer.rrset, "ttl", CACHE_DEFAULT_TTL_SECONDS) if answer.rrset else CACHE_DEFAULT_TTL_SECONDS

        results: List[Dict[str, Any]] = []
        for rdata in answer:
            if record_type in {"A", "AAAA", "CNAME", "NS"}:
                results.append({"value": str(rdata).rstrip(".")})
            elif record_type == "MX":
                results.append({"preference": int(rdata.preference), "exchange": str(rdata.exchange).rstrip(".")})
            elif record_type == "TXT":
                txt = rdata.to_text().strip('"')
                results.append({"value": txt})

        return latency_ms, results, int(ttl)

    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        latency_ms = int((time.perf_counter() - start) * 1000)
        return latency_ms, [], CACHE_DEFAULT_TTL_SECONDS
    except (dns.exception.Timeout, dns.resolver.YXDOMAIN, dns.resolver.NoNameservers) as e:
        raise RuntimeError(f"DNS lookup failed: {e}") from e
