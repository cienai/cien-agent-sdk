import { AdminClient } from './admin/index.js';
import { PublicClient } from './public/index.js';
import { HTTPTransport } from './transport.js';
export class CienClient {
    transport;
    public;
    admin;
    constructor(options) {
        this.transport = new HTTPTransport(options);
        this.public = new PublicClient(this.transport);
        this.admin = new AdminClient(this.transport);
    }
    setToken(token) {
        this.transport.setToken(token);
    }
}
export const CienAgentClient = CienClient;
