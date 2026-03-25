export function dropNullish(data) {
    return Object.fromEntries(Object.entries(data).filter(([, value]) => value !== null && value !== undefined));
}
export function buildUrl(baseUrl, path, params) {
    const url = new URL(path.replace(/^\//, ''), `${baseUrl.replace(/\/+$/, '')}/`);
    if (params) {
        for (const [key, value] of Object.entries(params)) {
            if (value === null || value === undefined)
                continue;
            if (Array.isArray(value)) {
                value.forEach((item) => url.searchParams.append(key, String(item)));
                continue;
            }
            url.searchParams.set(key, String(value));
        }
    }
    return url.toString();
}
export async function resolveHeaders(headers) {
    const resolved = typeof headers === 'function' ? await headers() : headers;
    return new Headers(resolved);
}
