import { EndpointGroup } from '../base.js';
export class AdminSyncLiveQueryAPI extends EndpointGroup {
    describe(payload) {
        return this.requestPost('/api/admin/sync_live_query/describe', {
            json: {
                coid: payload.coid,
                ...(payload.sync_id === undefined ? {} : { sync_id: payload.sync_id }),
                crm_entity: payload.crm_entity,
                column_names_only: payload.column_names_only ?? false,
            },
        });
    }
    query(payload) {
        return this.requestPost('/api/admin/sync_live_query/query', { json: payload });
    }
}
