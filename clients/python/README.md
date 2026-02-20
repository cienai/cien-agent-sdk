# cien-agent-sdk (Python)

Python client for `cien-agent-os` public and admin REST endpoints.

## Install (local)

```bash
cd clients/python
pip install -e .
```

## Quick usage

```python
from cien_agent_sdk import CienClient

client = CienClient(
    base_url="https://your-agent-os-host",
    token="<clerk-jwt-or-bearer-token>",
)

companies = client.public.companies.list()
print(companies)
```
