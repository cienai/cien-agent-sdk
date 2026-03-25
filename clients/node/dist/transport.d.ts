import type { RequestOptions, TokenProvider, TransportOptions, FetchLike } from './types.js';
export declare class HTTPTransport {
    readonly baseUrl: string;
    readonly timeout: number;
    readonly fetchImpl: FetchLike;
    readonly defaultHeaders?: TransportOptions['defaultHeaders'];
    private token?;
    constructor(options: TransportOptions);
    setToken(token?: TokenProvider): void;
    request<T = unknown>(method: string, path: string, options?: RequestOptions): Promise<T>;
}
