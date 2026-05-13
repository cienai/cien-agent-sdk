import { APIError, RequestError } from './errors.js'
import { hydrateJsonValue } from './hydration.js'
import type {
  RequestOptions,
  TokenProvider,
  TransportOptions,
  FetchLike,
} from './types.js'
import { buildUrl, resolveHeaders } from './utils.js'

function isAbortError(error: unknown): boolean {
  return error instanceof Error && error.name === 'AbortError'
}

function extractMessage(payload: unknown, fallback: string): string {
  if (payload && typeof payload === 'object' && 'detail' in payload) {
    const detail = (payload as { detail?: unknown }).detail
    if (typeof detail === 'string' && detail.trim()) return detail
    if (detail && typeof detail === 'object' && 'message' in detail) {
      const nested = (detail as { message?: unknown }).message
      if (typeof nested === 'string' && nested.trim()) return nested
    }
  }
  if (typeof payload === 'string' && payload.trim()) return payload
  return fallback
}

function isTokenExpiredPayload(payload: unknown): boolean {
  const msg = extractMessage(payload, '').toLowerCase()
  return (
    msg.includes('token_expired') ||
    msg.includes('tokenverificationerrorreason.token_expired') ||
    (msg.includes('expired') && msg.includes('token'))
  )
}

function createTimeoutSignal(timeout: number | undefined, externalSignal?: AbortSignal) {
  if (!timeout || timeout <= 0) {
    return { signal: externalSignal, cleanup: () => {} }
  }

  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeout)
  const abortExternal = () => controller.abort()

  if (externalSignal) {
    if (externalSignal.aborted) {
      controller.abort()
    } else {
      externalSignal.addEventListener('abort', abortExternal, { once: true })
    }
  }

  return {
    signal: controller.signal,
    cleanup: () => {
      clearTimeout(timer)
      if (externalSignal) {
        externalSignal.removeEventListener('abort', abortExternal)
      }
    },
  }
}

export class HTTPTransport {
  readonly baseUrl: string
  readonly timeout: number
  readonly fetchImpl: FetchLike
  readonly defaultHeaders?: TransportOptions['defaultHeaders']
  private token?: TokenProvider

  constructor(options: TransportOptions) {
    if (typeof globalThis.fetch !== 'function' && !options.fetch) {
      throw new RequestError(
        'Global fetch is not available. Pass a fetch implementation in the client options.'
      )
    }
    this.baseUrl = options.baseUrl.replace(/\/+$/, '')
    this.timeout = options.timeout ?? 60_000
    this.fetchImpl = options.fetch ?? globalThis.fetch.bind(globalThis)
    this.defaultHeaders = options.defaultHeaders
    this.token = options.token
  }

  setToken(token?: TokenProvider): void {
    this.token = token
  }

  async request<T = unknown>(method: string, path: string, options: RequestOptions = {}): Promise<T> {
    const url = buildUrl(this.baseUrl, path, options.params)
    const headers = await resolveHeaders(this.defaultHeaders)
    const requestHeaders = new Headers(headers)

    if (options.headers) {
      new Headers(options.headers).forEach((value, key) => requestHeaders.set(key, value))
    }

    const token = typeof this.token === 'function' ? await this.token() : this.token
    if (token && !requestHeaders.has('Authorization')) {
      requestHeaders.set('Authorization', `Bearer ${token}`)
    }

    let body: BodyInit | undefined
    if (options.json !== undefined) {
      body = JSON.stringify(options.json)
      if (!requestHeaders.has('Content-Type')) {
        requestHeaders.set('Content-Type', 'application/json')
      }
    } else if (options.body !== undefined) {
      body = options.body
    }

    const { signal, cleanup } = createTimeoutSignal(this.timeout, options.signal)

    try {
      const response = await this.fetchImpl(url, {
        method,
        headers: requestHeaders,
        body,
        signal,
      })

      if (response.status >= 400) {
        let payload: unknown
        try {
          payload = await response.json()
        } catch {
          payload = await response.text()
        }

        // If this is a 401 and it looks like the token expired, and we
        // have a token provider function, attempt to refresh once and retry.
        const tokenIsFunction = typeof this.token === 'function'
        if (response.status === 401 && tokenIsFunction && isTokenExpiredPayload(payload)) {
          try {
            const refreshed = await (this.token as () => Promise<string | null | undefined>)()
            if (refreshed) {
              // update Authorization header and retry once
              requestHeaders.set('Authorization', `Bearer ${refreshed}`)
              const retryResp = await this.fetchImpl(url, {
                method,
                headers: requestHeaders,
                body,
                signal,
              })
              if (retryResp.status >= 400) {
                let retryPayload: unknown
                try {
                  retryPayload = await retryResp.json()
                } catch {
                  retryPayload = await retryResp.text()
                }
                throw new APIError(
                  retryResp.status,
                  extractMessage(retryPayload, retryResp.statusText || 'Request failed'),
                  retryPayload
                )
              }
              // successful retry
              if (retryResp.status === 204) return undefined as T
              const retryContentType = retryResp.headers.get('content-type') || ''
              if (!retryContentType) {
                const text = await retryResp.text()
                return (text ? text : undefined) as T
              }
              if (retryContentType.includes('application/json')) {
                return hydrateJsonValue((await retryResp.json()) as T)
              }
              return (await retryResp.text()) as T
            }
          } catch {
            // fallthrough to raising original APIError below
          }
        }

        throw new APIError(
          response.status,
          extractMessage(payload, response.statusText || 'Request failed'),
          payload
        )
      }

      if (response.status === 204) {
        return undefined as T
      }

      const contentType = response.headers.get('content-type') || ''
      if (!contentType) {
        const text = await response.text()
        return (text ? text : undefined) as T
      }
      if (contentType.includes('application/json')) {
        return hydrateJsonValue((await response.json()) as T)
      }
      return (await response.text()) as T
    } catch (error) {
      if (error instanceof APIError) {
        throw error
      }
      const message = isAbortError(error)
        ? `Request timed out after ${this.timeout}ms`
        : error instanceof Error
          ? error.message
          : 'Request failed'
      throw new RequestError(message, { cause: error })
    } finally {
      cleanup()
    }
  }
}
