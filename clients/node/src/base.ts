import type { RequestOptions } from './types.js'
import { HTTPTransport } from './transport.js'

export class EndpointGroup {
  protected readonly transport: HTTPTransport

  constructor(transport: HTTPTransport) {
    this.transport = transport
  }

  protected requestGet<T = unknown>(
    path: string,
    options?: Omit<RequestOptions, 'json'>
  ): Promise<T> {
    return this.transport.request<T>('GET', path, options)
  }

  protected requestPost<T = unknown>(path: string, options?: RequestOptions): Promise<T> {
    return this.transport.request<T>('POST', path, options)
  }

  protected requestPut<T = unknown>(path: string, options?: RequestOptions): Promise<T> {
    return this.transport.request<T>('PUT', path, options)
  }

  protected requestPatch<T = unknown>(path: string, options?: RequestOptions): Promise<T> {
    return this.transport.request<T>('PATCH', path, options)
  }

  protected requestDelete<T = unknown>(
    path: string,
    options?: Omit<RequestOptions, 'json'>
  ): Promise<T> {
    return this.transport.request<T>('DELETE', path, options)
  }
}
