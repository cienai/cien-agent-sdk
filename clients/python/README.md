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

## Quick Start

```python
from cien_agent_sdk import CienClient

client = CienClient(
    base_url="https://your-agent-os-host",
    token="<clerk-jwt-or-bearer-token>",
)

companies = client.public.companies.list()
print(companies)
```

## Authentication

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
