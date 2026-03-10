# cien-agent-sdk (Node.js)

Node.js and Next.js client for `cien-agent-os` public and admin REST endpoints.

## Install

```bash
cd clients/node
pnpm install
```

## Quick Start

```ts
import { CienClient } from '@cien/cien-agent-sdk'

const client = new CienClient({
  baseUrl: 'https://your-agent-os-host',
  token: process.env.CIEN_BEARER_TOKEN,
})

const companies = await client.public.companies.search({
  limit: 25,
  order_by: 'name',
})
```

## Next.js Usage

The SDK uses standard `fetch`, so it works in:

- Next.js server components and route handlers
- browser code
- Node.js scripts

If you already have an authenticated wrapper, pass it as the SDK fetch implementation:

```ts
const client = new CienClient({
  baseUrl: process.env.NEXT_PUBLIC_DEFAULT_AGENTOS_ENDPOINT!,
  fetch: authFetch,
})
```

When consumed from a local Next.js app, add `@cien/cien-agent-sdk` to `transpilePackages` so Next transpiles the SDK source from the package.

## Error Handling

```ts
import { APIError, RequestError } from '@cien/cien-agent-sdk'

try {
  await client.admin.sync.list({ coid: 'example-coid' })
} catch (error) {
  if (error instanceof APIError) {
    console.error(error.statusCode, error.responseBody)
  } else if (error instanceof RequestError) {
    console.error(error.message)
  }
}
```

## Scope

This package mirrors the Python SDK endpoint groups for:

- `client.public.*`
- `client.admin.*`

It intentionally excludes AgentOS runtime routes such as `/agents`, `/sessions`, and `/api/agentic-definitions`.
