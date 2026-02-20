# Python SDK Usage

This guide covers common patterns for `cien_agent_sdk`.

## Client Initialization

```python
from cien_agent_sdk import CienClient

client = CienClient(
    base_url="https://your-agent-os-host",
    token="<bearer-token>",  # optional
    timeout=30.0,            # optional
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

## Endpoint References

- Public API methods: `clients/python/docs/PUBLIC_API.md`
- Admin API methods: `clients/python/docs/ADMIN_API.md`
