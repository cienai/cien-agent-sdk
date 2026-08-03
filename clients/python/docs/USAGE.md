# Python SDK Usage

This guide covers common patterns for `cien_agent_sdk`.

## Client Initialization

```python
from cien_agent_sdk import CienClient

client = CienClient(
    base_url="https://your-agent-os-host",
    token="<bearer-token>",  # optional
    timeout=60.0,            # optional; default is 60.0s
    max_retries=3,           # optional; GET retries enabled by default
    default_headers={        # optional
        "X-Request-Id": "job-123",
    },
)
```

## Service Account Authentication

```python
from cien_agent_sdk import CienClient

auth_client = CienClient(base_url="https://your-agent-os-host")
token_response = auth_client.public.users.issue_token(
    username="service-account-username",
    password="service-account-password",
)

client = CienClient(
    base_url="https://your-agent-os-host",
    token=token_response["token"],
)
```

## Rotating Tokens

```python
client.set_token("<new-bearer-token>")
```

## Error Model

All API calls can raise:

- `RequestError`: network/request execution failure.
- `APIError`: server returned HTTP status `>= 400`.

```python
from cien_agent_sdk import APIError, RequestError

try:
    me = client.public.users.whoami()
except APIError as exc:
    print(exc.status_code, exc.message, exc.response_body)
except RequestError as exc:
    print(str(exc))
```

## Common Patterns

- Use `.list(...)` methods for collection endpoints.
- Use `.lookup(...)` when you may have alternate identifiers (for example ID or name/email).
- Use `.update(...)` methods for partial updates.
- Use `.delete(...)` methods for removals.

## GET Retry Behavior

The SDK retries `GET` requests by default when it sees transient failures.

- `max_retries=3` by default
- Retryable HTTP statuses: `429`, `500`, `502`, `503`, `504`
- Retryable request failures: timeouts and connection errors
- Backoff schedule: `5s`, `10s`, `30s`, doubling thereafter, plus up to 20% jitter
- A `Retry-After` response header overrides the computed delay
- `400`, `401` (except transient token-verification server errors), and `404` are never retried
- Non-GET requests are not retried unless called with `retryable=True`

```python
client = CienClient(
    base_url="https://your-agent-os-host",
    token="<bearer-token>",
    max_retries=5,
)
```

## Metadata Caching

Schemas, config, CRM mappings, sync records, company lookups, and identity
(`whoami`) are cached for the life of the `CienClient` to cut repeated
AgentOS traffic within a pipeline run. Concurrent callers for the same key
share one in-flight request, and metadata request concurrency is capped
independently of any data-processing concurrency you manage yourself. See the
top-level `README.md` "Metadata Caching" section for the full cache/TTL table,
and `client.stats.snapshot()` for cache hit/miss and retry observability.

```python
client = CienClient(
    base_url="https://your-agent-os-host",
    token="<bearer-token>",
    metadata_max_concurrency=4,
    enable_metadata_cache=True,
)
```

## Endpoint References

- Public API methods: `clients/python/docs/PUBLIC_API.md`
- Admin API methods: `clients/python/docs/ADMIN_API.md`
