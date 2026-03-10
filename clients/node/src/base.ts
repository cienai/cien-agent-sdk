import type { RequestOptions } from './types'
import { HTTPTransport } from './transport'

export class EndpointGroup {
  protected readonly transport: HTTPTransport

  constructor(transport: HTTPTransport) {
    this.transport = transport
  }

  protected get<T = unknown>(path: string, options?: Omit<RequestOptions, 'json'>): Promise<T> {
    return this.transport.request<T>('GET', path, options)
  }

  protected post<T = unknown>(path: string, options?: RequestOptions): Promise<T> {
    return this.transport.request<T>('POST', path, options)
  }

  protected put<T = unknown>(path: string, options?: RequestOptions): Promise<T> {
    return this.transport.request<T>('PUT', path, options)
  }

  protected patch<T = unknown>(path: string, options?: RequestOptions): Promise<T> {
    return this.transport.request<T>('PATCH', path, options)
  }

  protected delete<T = unknown>(path: string, options?: Omit<RequestOptions, 'json'>): Promise<T> {
    return this.transport.request<T>('DELETE', path, options)
  }
}
