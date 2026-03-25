import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class AdminEnvironmentsAPI extends EndpointGroup {
    list(params) {
        return super.requestGet('/api/admin/environments', {
            params: { coid: params.coid, include_sync: params.include_sync ?? false, include_config: params.include_config ?? false },
        });
    }
    get(coid, params = {}) {
        return super.requestGet(`/api/admin/environments/${coid}`, {
            params: {
                environment: params.environment ?? 'staging',
                include_sync: params.include_sync ?? false,
                include_config: params.include_config ?? false,
            },
        });
    }
    create(payload) {
        return this.requestPost('/api/admin/environments', {
            params: { environment: payload.environment ?? 'staging' },
            json: { data: payload.data },
        });
    }
    update(coid, payload) {
        return this.requestPatch(`/api/admin/environments/${coid}`, {
            params: { environment: payload.environment ?? 'staging' },
            json: { updates: payload.updates },
        });
    }
    delete(coid, params = {}) {
        return super.requestDelete(`/api/admin/environments/${coid}`, {
            params: { environment: params.environment ?? 'staging' },
        });
    }
    copy(coid, payload = {}) {
        return this.requestPost(`/api/admin/environments/${coid}/copy`, {
            json: dropNullish({
                source_environment: payload.source_environment ?? 'prod',
                destination_environment: payload.destination_environment ?? 'staging',
                include_sync: payload.include_sync ?? true,
                overwrite_sync: payload.overwrite_sync ?? true,
            }),
        });
    }
}
