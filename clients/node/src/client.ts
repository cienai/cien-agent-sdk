import { AdminClient } from './admin/index.js'
import { PublicClient } from './public/index.js'
import { HTTPTransport } from './transport.js'
import type { TokenProvider, TransportOptions } from './types.js'

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
