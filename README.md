# cien-agent-sdk

SDK repository for `cien-agent-os` API clients.

## Scope

This SDK targets:

- Public endpoints under `/api/*`
- Admin endpoints under `/api/admin/*`

This SDK intentionally excludes AgentOS runtime/Agno-specific routes (for example session/memory and `/api/agentic-definitions` routes).

## Repository Structure

- `clients/python`: Python SDK (implemented)
- `clients/node`: Node.js SDK scaffold (not implemented yet)
- `scripts/generate_endpoint_catalog.py`: route scanner for `cien-agent-os`
- `spec/cien-agent-os-endpoints.json`: generated route catalog used for SDK maintenance

## Python SDK

### Install from GitHub

```bash
pip install "git+https://github.com/cienai/cien-agent-sdk.git@main#subdirectory=clients/python"
```

### Install (editable local clone)

```bash
git clone https://github.com/cienai/cien-agent-sdk.git
cd cien-agent-sdk
cd clients/python
pip install -e .
```

### Basic Usage

```python
from cien_agent_sdk import CienClient

auth_client = CienClient(base_url="https://your-cien-agent-os-host")
token_response = auth_client.public.users.issue_token(
    username="cien-service-account",
    password="<password>",
)

client = CienClient(
    base_url="https://your-cien-agent-os-host",
    token=token_response["token"],
)

# Public APIs
version = client.public.version.get()
companies = client.public.companies.list()
whoami = client.public.users.whoami()

# Admin APIs
admin_companies = client.admin.companies.list()
sync_rows = client.admin.sync.list(coid="my-company-id")
```

### Python Docs

- `clients/python/README.md`
- `clients/python/docs/USAGE.md`
- `clients/python/docs/PUBLIC_API.md`
- `clients/python/docs/ADMIN_API.md`

### Getting a Bearer Token

Use one of these approaches:

1. Service account username/password:
   - Call `POST /api/users/token` with `username` and `password`.
   - Use the returned `token` as your bearer token.
2. Interactive user auth with Clerk:
   - Obtain a Clerk JWT in your app.
   - Pass that JWT as the SDK `token`.

### Service-account login (username/password)

```python
from cien_agent_sdk import CienClient

auth_client = CienClient(base_url="https://your-cien-agent-os-host")
token_response = auth_client.public.users.issue_token(
    username="cien-service-account",
    password="<password>",
)

client = CienClient(
    base_url="https://your-cien-agent-os-host",
    token=token_response["token"],
)
```

### Auth and headers

- The client sets `Authorization: Bearer <token>` when `token` is provided.
- You can pass additional default headers via `default_headers=`.
- You can rotate auth at runtime using `client.set_token(...)`.

## Keeping SDK Current With `cien-agent-os`

1. Generate updated route catalog:

```bash
./scripts/generate_endpoint_catalog.py \
  --agent-os-path /path/to/cien-agent-os \
  --output spec/cien-agent-os-endpoints.json
```

2. Compare changed routes in `spec/cien-agent-os-endpoints.json`.
3. Update the corresponding SDK modules under:
   - `clients/python/src/cien_agent_sdk/public/*`
   - `clients/python/src/cien_agent_sdk/admin/*`
4. Add/update tests in `clients/python/tests` as needed.

This keeps endpoint discovery automated while preserving explicit, readable client method definitions.

## Planned Next Step

- Implement Node.js SDK under `clients/node` using the same module layout as Python.
