# DNS Resolver API

A production-style DNS Resolver API built with FastAPI. Supports multiple DNS record lookups with TTL-based caching, latency tracking, and service-level metrics.

## Overview

This project provides a high-performance DNS resolution service exposed via a REST API. It is designed to simulate real-world backend systems by incorporating caching strategies, performance tracking, and structured responses.

The API resolves various DNS record types, caches responses based on TTL, and tracks latency to provide insights into system performance.

## Features

- Resolve DNS records:
  - A
  - AAAA
  - MX
  - TXT
  - CNAME
  - NS
- TTL-based caching to reduce redundant lookups
- Latency tracking for performance monitoring
- Structured JSON API responses
- Error handling and validation
- Lightweight and fast API built with FastAPI

## Tech Stack

- FastAPI (Python)
- DNS resolution libraries (e.g., dnspython)
- In-memory caching
- REST API architecture

## API Endpoints

### Resolve DNS Record
GET /resolve?domain=example.com&type=A

#### Query Parameters
- `domain` (string) – Domain to resolve
- `type` (string) – Record type (A, AAAA, MX, TXT, CNAME, NS)

#### Example Response

```json
{
  "domain": "example.com",
  "record_type": "A",
  "records": ["93.184.216.34"],
  "ttl": 300,
  "cached": true,
  "latency_ms": 12
}
```
Service Metrics
```
GET /metrics
```
Example Response
```
{
  "total_requests": 120,
  "cache_hits": 85,
  "average_latency_ms": 15
}
```
### Project Structure
app/        → API routes, services, DNS logic

### Prerequisites
Python 3.9+
pip

### Getting Started
```
cd dns-resolver-api
pip install -r requirements.txt
uvicorn main:app --reload
```
### How It Works

Client sends a request to resolve a DNS record
The system checks if the result exists in cache
If cached and valid → returns cached result
If not → performs DNS lookup
Stores result with TTL
Tracks latency and updates metrics
Returns structured response

### Future Improvements

Persistent caching (Redis)
Rate limiting
Authentication (API keys)
Docker containerization
Logging and monitoring integration
Horizontal scaling support

### Author
Elisha Gilbert
Email: elishagilbert60@gmail.com
