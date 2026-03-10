export type MaybePromise<T> = T | Promise<T>

export type JsonPrimitive = string | number | boolean | null

export type JsonValue = JsonPrimitive | JsonObject | JsonArray

export interface JsonObject {
  [key: string]: JsonValue
}

export interface JsonArray extends Array<JsonValue> {}

export type QueryValue =
  | string
  | number
  | boolean
  | Array<string | number | boolean>
  | null
  | undefined

export type QueryParams = Record<string, QueryValue>

export type RequestHeaders =
  | HeadersInit
  | (() => MaybePromise<HeadersInit | undefined>)

export type TokenProvider = string | null | undefined | (() => MaybePromise<string | null | undefined>)

export type FetchLike = (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>

export interface RequestOptions {
  params?: QueryParams
  json?: unknown
  headers?: HeadersInit
  signal?: AbortSignal
}

export interface TransportOptions {
  baseUrl: string
  token?: TokenProvider
  timeout?: number
  defaultHeaders?: RequestHeaders
  fetch?: FetchLike
}

export type PermissionRole = 'view' | 'manage' | 'owner'
export type UserCompanyRoleFilter = PermissionRole | 'any'
export type CompanyUserRoleFilter = 'manage' | 'owner' | 'any'
