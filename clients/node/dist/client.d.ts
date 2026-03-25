import { AdminClient } from './admin/index.js';
import { PublicClient } from './public/index.js';
import { HTTPTransport } from './transport.js';
import type { TokenProvider, TransportOptions } from './types.js';
export declare class CienClient {
    readonly transport: HTTPTransport;
    readonly public: PublicClient;
    readonly admin: AdminClient;
    constructor(options: TransportOptions);
    setToken(token?: TokenProvider): void;
}
export declare const CienAgentClient: typeof CienClient;
