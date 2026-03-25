import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class AdminSyncSourceDefinitionsAPI extends EndpointGroup {
    list(params = {}) {
        return super.requestGet('/api/admin/sync-source-definitions', {
            params: dropNullish(params),
        });
    }
    get(definitionId) {
        return super.requestGet(`/api/admin/sync-source-definitions/${definitionId}`);
    }
    getBySourceType(sourceType) {
        return super.requestGet(`/api/admin/sync-source-definitions/source-type/${sourceType}`);
    }
    create(payload) {
        return this.requestPost('/api/admin/sync-source-definitions', {
            json: {
                ...payload,
                required_settings: payload.required_settings ?? [],
                is_active: payload.is_active ?? true,
            },
        });
    }
    update(definitionId, payload) {
        return this.requestPatch(`/api/admin/sync-source-definitions/${definitionId}`, { json: payload });
    }
    async delete(definitionId) {
        await super.requestDelete(`/api/admin/sync-source-definitions/${definitionId}`);
    }
}
