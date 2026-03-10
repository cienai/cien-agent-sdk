import { EndpointGroup } from '../base'
import { dropNullish } from '../utils'

export class AdminCompaniesAPI extends EndpointGroup {
  list(params: {
    partner_id?: string
    clerk_org_id?: string
    selected_columns?: string[]
    filters?: string
    order_by?: string
    limit?: number
    natural_query?: string
  } = {}) {
    return super.get<Array<Record<string, unknown>>>('/api/admin/companies', {
      params: dropNullish(params),
    })
  }

  search(payload: {
    partner_id?: string
    clerk_org_id?: string
    selected_columns?: string[]
    filters?: Record<string, unknown>
    order_by?: string
    limit?: number
    natural_query?: string
  } = {}) {
    return this.post<Array<Record<string, unknown>>>('/api/admin/companies/search', {
      json: dropNullish(payload),
    })
  }

  create(payload: { data: Record<string, unknown>; selected_columns?: string[] }) {
    return this.post<Record<string, unknown>>('/api/admin/companies', { json: payload })
  }

  get(coid: string, params: { selected_columns?: string[] } = {}) {
    return super.get<Record<string, unknown>>('/api/admin/companies/companies', {
      params: dropNullish({ coid, ...params }),
    })
  }

  lookup(params: {
    company_id?: string
    company_name?: string
    selected_columns?: string[]
  }) {
    return super.get<Record<string, unknown>>('/api/admin/companies/lookup', {
      params: dropNullish(params),
    })
  }

  update(
    companyId: string,
    payload: { updates: Record<string, unknown>; selected_columns?: string[] }
  ) {
    return this.patch<Record<string, unknown>>(`/api/admin/companies/${companyId}`, {
      json: payload,
    })
  }

  delete(companyId: string) {
    return super.delete<Record<string, unknown>>(`/api/admin/companies/${companyId}`)
  }
}
