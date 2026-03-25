import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class PublicConfigAPI extends EndpointGroup {
    list(params) {
        return super.requestGet('/api/config', {
            params: dropNullish(params),
        });
    }
    get(params) {
        return super.requestGet(`/api/config/${params.coid}/${params.key}`, {
            params: { convert_dtypes: params.convert_dtypes ?? false },
        });
    }
    save(payload) {
        return this.requestPost(`/api/config/${payload.coid}`, {
            json: { key: payload.key, type: payload.config_type, value: payload.value },
        });
    }
    update(payload) {
        return this.requestPut(`/api/config/${payload.coid}`, {
            json: { config: payload.config },
        });
    }
    async delete(params) {
        await super.requestDelete(`/api/config/${params.coid}/${params.key}`);
    }
}
