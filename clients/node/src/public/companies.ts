import { EndpointGroup } from '../base.js'
import { dropNullish } from '../utils.js'

export class PublicCompaniesAPI extends EndpointGroup {
  list(params: {
    selected_columns?: string[]
    filters?: string
    order_by?: string
    limit?: number
    natural_query?: string
  } = {}) {
    return super.get<Array<Record<string, unknown>>>('/api/companies', {
      params: dropNullish(params),
    })
  }

  search(payload: {
    selected_columns?: string[]
    filters?: Record<string, unknown>
    order_by?: string
    limit?: number
    natural_query?: string
    clerk_org_id?: string
  } = {}) {
    return this.post<Array<Record<string, unknown>>>('/api/companies/search', {
      json: dropNullish(payload),
    })
  }

  get(coid: string, params: { selected_columns?: string[] } = {}) {
    return super.get<Record<string, unknown>>('/api/companies/companies', {
      params: dropNullish({ coid, ...params }),
    })
  }

  lookup(params: {
    company_id?: string
    company_name?: string
    selected_columns?: string[]
  }) {
    return super.get<Record<string, unknown>>('/api/companies/lookup', {
      params: dropNullish(params),
    })
  }

  update(
    companyId: string,
    payload: { updates: Record<string, unknown>; selected_columns?: string[] }
  ) {
    return this.patch<Record<string, unknown>>(`/api/companies/${companyId}`, {
      json: payload,
    })
  }

  delete(companyId: string) {
    return super.delete<Record<string, unknown>>(`/api/companies/${companyId}`)
  }
}
