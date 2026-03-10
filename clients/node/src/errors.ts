export class CienAgentSDKError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'CienAgentSDKError'
  }
}

export class APIError extends CienAgentSDKError {
  statusCode: number
  responseBody: unknown

  constructor(statusCode: number, message: string, responseBody?: unknown) {
    super(`HTTP ${statusCode}: ${message}`)
    this.name = 'APIError'
    this.statusCode = statusCode
    this.responseBody = responseBody
  }
}

export class RequestError extends CienAgentSDKError {
  cause?: unknown

  constructor(message: string, options?: { cause?: unknown }) {
    super(message)
    this.name = 'RequestError'
    this.cause = options?.cause
  }
}
