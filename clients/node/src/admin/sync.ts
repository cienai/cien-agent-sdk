import { APIError } from '../errors.js'
import { EndpointGroup } from '../base.js'
import { dropNullish } from '../utils.js'

export interface ResetSyncResponse {
  message: string
  coid: string
  entity: string
  status_cleared: boolean
  deleted_files: string[]
  errors: string[]
}

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
    return super.requestGet<Array<Record<string, unknown>>>('/api/admin/sync', {
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
      return await super.requestGet<Record<string, unknown>>(`/api/admin/sync/by-token/${syncToken}`)
    } catch (error) {
      if (error instanceof APIError && error.statusCode === 404) {
        return null
      }
      throw error
    }
  }

  get(syncId: number) {
    return super.requestGet<Record<string, unknown>>(`/api/admin/sync/${syncId}`)
  }

  create(payload: Record<string, unknown>) {
    return this.requestPost<Record<string, unknown>>('/api/admin/sync', { json: payload })
  }

  update(syncId: number, payload: Record<string, unknown>) {
    return this.requestPatch<Record<string, unknown>>(`/api/admin/sync/${syncId}`, {
      json: payload,
    })
  }

  async delete(syncId: number) {
    await super.requestDelete(`/api/admin/sync/${syncId}`)
  }

  reset(payload: { coid: string; crm_entity: string; reset_delta?: boolean }) {
    return this.requestPost<ResetSyncResponse>('/api/admin/sync/reset', {
      json: {
        coid: payload.coid,
        crm_entity: payload.crm_entity,
        reset_delta: payload.reset_delta ?? true,
      },
    })
  }
}
