import { AdminClient } from './admin/index'
import { PublicClient } from './public/index'
import { HTTPTransport } from './transport'
import type { TokenProvider, TransportOptions } from './types'

export class CienClient {
  readonly transport: HTTPTransport
  readonly public: PublicClient
  readonly admin: AdminClient

  constructor(options: TransportOptions) {
    this.transport = new HTTPTransport(options)
    this.public = new PublicClient(this.transport)
    this.admin = new AdminClient(this.transport)
  }

  setToken(token?: TokenProvider) {
    this.transport.setToken(token)
  }
}

export const CienAgentClient = CienClient
