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

- Retryable HTTP statuses: `429`, `502`, `503`, `504`
- Retryable request failures: connection errors and timeouts
- Default request timeout: `60s`
- Delay schedule: `5s`, `10s`, `30s`
- Non-GET methods are not retried

```python
client = CienClient(
    base_url="https://your-agent-os-host",
    token="<clerk-jwt-or-bearer-token>",
    max_retries=5,
)
```

## Clerk API Key Helpers

```python
from cien_agent_sdk import ClerkHelper

clerk = ClerkHelper(bearer_auth="<CLERK_SECRET_KEY>")

user_id = clerk.get_user_id_by_email("user@example.com")
api_key = clerk.create_user_api_key(user_id=user_id)
secret = clerk.get_user_api_key_secret(user_id=user_id)
```
