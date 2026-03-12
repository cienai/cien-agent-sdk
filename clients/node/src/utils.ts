import type { QueryParams, RequestHeaders } from './types.js'

export function dropNullish<T extends Record<string, unknown>>(data: T): Partial<T> {
  return Object.fromEntries(
    Object.entries(data).filter(([, value]) => value !== null && value !== undefined)
  ) as Partial<T>
}

export function buildUrl(baseUrl: string, path: string, params?: QueryParams): string {
  const url = new URL(path.replace(/^\//, ''), `${baseUrl.replace(/\/+$/, '')}/`)
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value === null || value === undefined) continue
      if (Array.isArray(value)) {
        value.forEach((item) => url.searchParams.append(key, String(item)))
        continue
      }
      url.searchParams.set(key, String(value))
    }
  }
  return url.toString()
}

export async function resolveHeaders(
  headers: RequestHeaders | undefined
): Promise<Headers> {
  const resolved = typeof headers === 'function' ? await headers() : headers
  return new Headers(resolved)
}
