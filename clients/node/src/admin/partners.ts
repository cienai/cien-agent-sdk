import { EndpointGroup } from '../base.js'
import { dropNullish } from '../utils.js'

export class AdminPartnersAPI extends EndpointGroup {
  list(params: {
    include_deleted?: boolean
    include_inactive?: boolean
    show_all?: boolean
  } = {}) {
    return super.requestGet<Array<Record<string, unknown>>>('/api/admin/partners', {
      params: {
        include_deleted: params.include_deleted ?? false,
        include_inactive: params.include_inactive ?? true,
        show_all: params.show_all ?? false,
      },
    })
  }

  get(partnerId: number) {
    return super.requestGet<Record<string, unknown>>(`/api/admin/partners/${partnerId}`)
  }

  create(payload: { name: string; clerk_org_id?: string; is_active?: boolean }) {
    return this.requestPost<Record<string, unknown>>('/api/admin/partners', {
      json: dropNullish({ ...payload, is_active: payload.is_active ?? true }),
    })
  }

  update(
    partnerId: number,
    payload: {
      name?: string
      clerk_org_id?: string
      clerk_org_slug?: string
      max_allowed_memberships?: number
      public_metadata?: Record<string, unknown>
      private_metadata?: Record<string, unknown>
      is_active?: boolean
      is_deleted?: boolean
    }
  ) {
    return this.requestPatch<Record<string, unknown>>(`/api/admin/partners/${partnerId}`, {
      json: dropNullish(payload),
    })
  }

  delete(partnerId: number) {
    return super.requestDelete<Record<string, unknown>>(`/api/admin/partners/${partnerId}`)
  }
}
