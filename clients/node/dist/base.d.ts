import type { RequestOptions } from './types.js';
import { HTTPTransport } from './transport.js';
export declare class EndpointGroup {
    protected readonly transport: HTTPTransport;
    constructor(transport: HTTPTransport);
    protected requestGet<T = unknown>(path: string, options?: Omit<RequestOptions, 'json'>): Promise<T>;
    protected requestPost<T = unknown>(path: string, options?: RequestOptions): Promise<T>;
    protected requestPut<T = unknown>(path: string, options?: RequestOptions): Promise<T>;
    protected requestPatch<T = unknown>(path: string, options?: RequestOptions): Promise<T>;
    protected requestDelete<T = unknown>(path: string, options?: Omit<RequestOptions, 'json'>): Promise<T>;
}
