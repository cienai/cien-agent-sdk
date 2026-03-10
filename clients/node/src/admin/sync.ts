import { APIError } from '../errors'
import { EndpointGroup } from '../base'
import { dropNullish } from '../utils'

export class AdminSyncAPI extends EndpointGroup {
  list(params: {
    coid?: string
    sync_token?: string
    sync_type?: string
    is_active?: boolean
  }) {
    if (!params.coid && !params.sync_token) {
      throw new TypeError('Either coid or sync_token is required')
    }
    return super.get<Array<Record<string, unknown>>>('/api/admin/sync', {
      params: dropNullish({
        coid: params.coid,
        sync_token: params.sync_token,
        sync_type: params.sync_type,
        _sys_isactive: params.is_active,
      }),
    })
  }

  async getBySyncToken(syncToken: string) {
    try {
      return await super.get<Record<string, unknown>>(`/api/admin/sync/by-token/${syncToken}`)
    } catch (error) {
      if (error instanceof APIError && error.statusCode === 404) {
        return null
      }
      throw error
    }
  }

  get(syncId: number) {
    return super.get<Record<string, unknown>>(`/api/admin/sync/${syncId}`)
  }

  create(payload: Record<string, unknown>) {
    return this.post<Record<string, unknown>>('/api/admin/sync', { json: payload })
  }

  update(syncId: number, payload: Record<string, unknown>) {
    return this.patch<Record<string, unknown>>(`/api/admin/sync/${syncId}`, {
      json: payload,
    })
  }

  async delete(syncId: number) {
    await super.delete(`/api/admin/sync/${syncId}`)
  }

  reset(payload: { coid: string; crm_entity: string; reset_delta?: boolean }) {
    return this.post<Record<string, unknown>>('/api/admin/sync/reset', {
      json: {
        coid: payload.coid,
        crm_entity: payload.crm_entity,
        reset_delta: payload.reset_delta ?? true,
      },
    })
  }
}
