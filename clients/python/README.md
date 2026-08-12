# cien-agent-sdk (Python)

Python client for `cien-agent-os` public and admin REST endpoints.

## Install

### Local editable install

```bash
cd clients/python
pip install -e .
```

### Install from GitHub

```bash
pip install "git+https://github.com/cienai/cien-agent-sdk.git@main#subdirectory=clients/python"
```

### Optional: Clerk helpers

```bash
pip install -e ".[clerk]"
```

## Quick Start

```python
from cien_agent_sdk import CienClient

client = CienClient(
    base_url="https://your-agent-os-host",
    token="<clerk-jwt-or-bearer-token>",
    max_retries=3,
)

companies = client.public.companies.list()
print(companies)
```

## Authentication

> Need credentials or auth setup details? Contact Cien to get authentication information for your environment.

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

## Documentation

- Usage guide: `clients/python/docs/USAGE.md`
- Public APIs: `clients/python/docs/PUBLIC_API.md`
- Admin APIs: `clients/python/docs/ADMIN_API.md`

## Error Handling

```python
from cien_agent_sdk import APIError, RequestError

try:
    rows = client.admin.sync.list(coid="example-coid")
except APIError as exc:
    print(exc.status_code, exc.message, exc.response_body)
except RequestError as exc:
    print(str(exc))
```

## GET Retry Defaults

`CienClient` enables GET retries by default with `max_retries=3`.

- Retryable HTTP statuses: `429`, `500`, `502`, `503`, `504`
- Retryable request failures: connection errors and timeouts
- Default request timeout: `60s`
- Delay schedule: `5s`, `10s`, `30s`, doubling thereafter, plus up to 20% random jitter
- A `Retry-After` response header (delta-seconds or HTTP-date) overrides the computed delay
- `400`, `401` (except transient token-verification server errors), and `404` are never retried
- Non-GET methods are not retried unless the call passes `retryable=True`

```python
client = CienClient(
    base_url="https://your-agent-os-host",
    token="<clerk-jwt-or-bearer-token>",
    max_retries=5,
)
```

## Metadata Caching

To cut repeated traffic to a small set of slow-changing AgentOS metadata
endpoints, `CienClient` caches them for the life of the client (one client per
pipeline run), coalesces concurrent requests for the same key into a single
outbound call, and bounds concurrent metadata requests independently of any
data-processing concurrency the caller manages itself.

| Endpoint(s) | Cache scope | TTL |
|---|---|---|
| `public.schemas.load_schema` | `(coid, cien_entity)` | 20 min, invalidated by `initialize_schemas` |
| `public.config.list` / `.get` | `(coid, key, level, ...)` | 20 min, invalidated by `save`/`update`/`delete` |
| `admin.mappings.list_crm_entities` / `.get_crm_mappings` / `.get_cien_entity` | `(coid, ...)` | run-scoped, invalidated by `save_crm_mappings` |
| `admin.sync.list` / `.get` | `(coid/sync_id, ...)` | 7.5 min, invalidated by sync mutations |
| `admin.sync_mappings.get_*` | `(sync_id, ...)` | run-scoped, invalidated by the matching `set_*` |
| `admin.companies.get` | `(coid, ...)` | 7.5 min, invalidated by `update`/`delete` |
| `public.users.whoami` | per session | run-scoped |

Every other call (mutations, job logs, live query, PowerBI, etc.) is
unaffected and always hits the network.

```python
client = CienClient(
    base_url="https://your-agent-os-host",
    token="<clerk-jwt-or-bearer-token>",
    metadata_max_concurrency=4,  # bound concurrent outbound metadata requests
    enable_metadata_cache=True,  # set False to bypass caching entirely
    run_id="airflow-run-id",     # tags every request with X-Cien-Run-Id
)

client.public.schemas.load_schema(coid="co-1", cien_entity="companies")  # network call
client.public.schemas.load_schema(coid="co-1", cien_entity="companies")  # cache hit

print(client.stats.snapshot())
# {"cache_hits": 1, "cache_misses": 1, "coalesced": 0, "metadata_requests_total": 1,
#  "peak_concurrency": 1, "retries_by_status": {}, "count_429": 0}
```

Every request also carries a stable `X-Cien-Client-Id` header (auto-generated
once per client, or pass `client_id=` to fix it), so AgentOS can attribute
traffic across retries and cache hits/misses to the same client.

## Clerk API Key Helpers

```python
from cien_agent_sdk import ClerkHelper

clerk = ClerkHelper(bearer_auth="<CLERK_SECRET_KEY>")

user_id = clerk.get_user_id_by_email("user@example.com")
api_key = clerk.create_user_api_key(user_id=user_id)
secret = clerk.get_user_api_key_secret(user_id=user_id)
```
