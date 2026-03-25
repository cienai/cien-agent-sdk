const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const DATETIME_RE = /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$/;
function hydrateString(value) {
    if (DATETIME_RE.test(value) || DATE_RE.test(value)) {
        const hydrated = new Date(value);
        if (!Number.isNaN(hydrated.getTime())) {
            return hydrated;
        }
    }
    return value;
}
export function hydrateJsonValue(value) {
    if (typeof value === 'string') {
        return hydrateString(value);
    }
    if (Array.isArray(value)) {
        return value.map((item) => hydrateJsonValue(item));
    }
    if (value && typeof value === 'object') {
        return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, hydrateJsonValue(item)]));
    }
    return value;
}
