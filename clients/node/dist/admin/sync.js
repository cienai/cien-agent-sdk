import { APIError } from '../errors.js';
import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class AdminSyncAPI extends EndpointGroup {
    list(params) {
        if (!params.coid && !params.sync_token) {
            throw new TypeError('Either coid or sync_token is required');
        }
        return super.requestGet('/api/admin/sync', {
            params: dropNullish({
                coid: params.coid,
                sync_token: params.sync_token,
                sync_type: params.sync_type,
                _sys_isactive: params.is_active,
            }),
        });
    }
    async getBySyncToken(syncToken) {
        try {
            return await super.requestGet(`/api/admin/sync/by-token/${syncToken}`);
        }
        catch (error) {
            if (error instanceof APIError && error.statusCode === 404) {
                return null;
            }
            throw error;
        }
    }
    get(syncId) {
        return super.requestGet(`/api/admin/sync/${syncId}`);
    }
    create(payload) {
        return this.requestPost('/api/admin/sync', { json: payload });
    }
    update(syncId, payload) {
        return this.requestPatch(`/api/admin/sync/${syncId}`, {
            json: payload,
        });
    }
    async delete(syncId) {
        await super.requestDelete(`/api/admin/sync/${syncId}`);
    }
    reset(payload) {
        return this.requestPost('/api/admin/sync/reset', {
            json: {
                sync_id: payload.sync_id,
                crm_entity: payload.crm_entity,
                reset_delta: payload.reset_delta ?? true,
            },
        });
    }
}
