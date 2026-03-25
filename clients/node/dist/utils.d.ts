import type { QueryParams, RequestHeaders } from './types.js';
export declare function dropNullish<T extends Record<string, unknown>>(data: T): Partial<T>;
export declare function buildUrl(baseUrl: string, path: string, params?: QueryParams): string;
export declare function resolveHeaders(headers: RequestHeaders | undefined): Promise<Headers>;
