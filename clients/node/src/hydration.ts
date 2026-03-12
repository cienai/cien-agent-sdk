const DATE_RE = /^\d{4}-\d{2}-\d{2}$/
const DATETIME_RE =
  /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$/

function hydrateString(value: string): unknown {
  if (DATETIME_RE.test(value) || DATE_RE.test(value)) {
    const hydrated = new Date(value)
    if (!Number.isNaN(hydrated.getTime())) {
      return hydrated
    }
  }
  return value
}

export function hydrateJsonValue<T>(value: T): T {
  if (typeof value === 'string') {
    return hydrateString(value) as T
  }
  if (Array.isArray(value)) {
    return value.map((item) => hydrateJsonValue(item)) as T
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>).map(([key, item]) => [key, hydrateJsonValue(item)])
    ) as T
  }
  return value
}
