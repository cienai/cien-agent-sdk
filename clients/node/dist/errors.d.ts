export declare class CienAgentSDKError extends Error {
    constructor(message: string);
}
export declare class APIError extends CienAgentSDKError {
    statusCode: number;
    responseBody: unknown;
    constructor(statusCode: number, message: string, responseBody?: unknown);
}
export declare class RequestError extends CienAgentSDKError {
    cause?: unknown;
    constructor(message: string, options?: {
        cause?: unknown;
    });
}
