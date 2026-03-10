import { EndpointGroup } from '../base.js'
import { dropNullish } from '../utils.js'

export class PublicUsersAPI extends EndpointGroup {
  issueToken(payload: { username: string; password: string }) {
    return this.post<Record<string, unknown>>('/api/users/token', { json: payload })
  }

  upsert(payload: {
    clerk_user_id: string
    clerk_org_id: string
    clerk_session_id?: string
    email?: string
    display_name?: string
    given_name?: string
    surname?: string
    clerk_raw?: Record<string, unknown>
    partner_id?: number
  }) {
    return this.post<Record<string, unknown>>('/api/users/upsert', {
      json: dropNullish({ ...payload, clerk_raw: payload.clerk_raw ?? {} }),
    })
  }

  invite(payload: { identifier: string; partner_id?: number }) {
    return this.post<Record<string, unknown>>('/api/users/invite', {
      json: dropNullish(payload),
    })
  }

  setCompanyPermission(payload: { email: string; coid: string; permissions: string }) {
    return this.post<Record<string, unknown>>('/api/users/company-permissions/set', {
      json: payload,
    })
  }

  removeCompanyPermission(payload: { email: string; coid: string }) {
    return this.post<Record<string, unknown>>('/api/users/company-permissions/remove', {
      json: payload,
    })
  }

  list(params: {
    clerk_org_id?: string
    partner_id?: number
    search?: string
    include_deleted?: boolean
    only_active?: boolean
    limit?: number
    offset?: number
  } = {}) {
    return this.get<Array<Record<string, unknown>>>('/api/users', {
      params: dropNullish({
        include_deleted: false,
        only_active: true,
        limit: 50,
        offset: 0,
        ...params,
      }),
    })
  }

  lookup(params: {
    clerk_user_id?: string
    clerk_org_id?: string
    email?: string
    include_deleted?: boolean
  }) {
    return this.get<Record<string, unknown>>('/api/users/lookup', {
      params: dropNullish({ include_deleted: false, ...params }),
    })
  }

  whoAmI() {
    return this.get<Record<string, unknown>>('/whoami')
  }
}
