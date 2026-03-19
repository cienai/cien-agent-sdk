import { EndpointGroup } from '../base.js'

export class AdminSyncLiveQueryAPI extends EndpointGroup {
  describe(payload: { coid: string; crm_entity: string; column_names_only?: boolean }) {
    return this.requestPost<unknown>('/api/admin/sync_live_query/describe', {
      json: {
        coid: payload.coid,
        crm_entity: payload.crm_entity,
        column_names_only: payload.column_names_only ?? false,
      },
    })
  }

  query(payload: { coid: string; crm_entity: string; query: string; limit?: number | string }) {
    return this.requestPost<unknown>('/api/admin/sync_live_query/query', { json: payload })
  }
}
