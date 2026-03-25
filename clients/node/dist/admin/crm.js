import { EndpointGroup } from '../base.js';
export class AdminCrmAPI extends EndpointGroup {
    describe(payload) {
        return this.requestPost('/api/admin/crm/describe', {
            json: {
                coid: payload.coid,
                table: payload.table,
                column_names_only: payload.column_names_only ?? false,
            },
        });
    }
    query(payload) {
        return this.requestPost('/api/admin/crm/query', { json: payload });
    }
}
