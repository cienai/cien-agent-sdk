export class EndpointGroup {
    transport;
    constructor(transport) {
        this.transport = transport;
    }
    requestGet(path, options) {
        return this.transport.request('GET', path, options);
    }
    requestPost(path, options) {
        return this.transport.request('POST', path, options);
    }
    requestPut(path, options) {
        return this.transport.request('PUT', path, options);
    }
    requestPatch(path, options) {
        return this.transport.request('PATCH', path, options);
    }
    requestDelete(path, options) {
        return this.transport.request('DELETE', path, options);
    }
}
