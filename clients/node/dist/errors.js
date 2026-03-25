export class CienAgentSDKError extends Error {
    constructor(message) {
        super(message);
        this.name = 'CienAgentSDKError';
    }
}
export class APIError extends CienAgentSDKError {
    statusCode;
    responseBody;
    constructor(statusCode, message, responseBody) {
        super(`HTTP ${statusCode}: ${message}`);
        this.name = 'APIError';
        this.statusCode = statusCode;
        this.responseBody = responseBody;
    }
}
export class RequestError extends CienAgentSDKError {
    cause;
    constructor(message, options) {
        super(message);
        this.name = 'RequestError';
        this.cause = options?.cause;
    }
}
