import { EndpointGroup } from '../base'

export class AdminCrmAPI extends EndpointGroup {
  describe(payload: { coid: string; table: string; column_names_only?: boolean }) {
    return this.requestPost<unknown>('/api/admin/crm/describe', {
      json: {
        coid: payload.coid,
        table: payload.table,
        column_names_only: payload.column_names_only ?? false,
      },
    })
  }

  query(payload: { coid: string; table: string; query: string; limit?: number }) {
    return this.requestPost<unknown>('/api/admin/crm/query', { json: payload })
  }
}
