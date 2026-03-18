import { EndpointGroup } from '../base.js'
import { dropNullish } from '../utils.js'

export class AdminEnvironmentsAPI extends EndpointGroup {
  list(params: { coid: string; include_sync?: boolean, include_config?: boolean }) {
    return super.requestGet<Record<string, unknown>>('/api/admin/environments', {
      params: { coid: params.coid, include_sync: params.include_sync ?? false, include_config: params.include_config ?? false },
    })
  }

  get(coid: string, params: { environment?: string; include_sync?: boolean, include_config?: boolean } = {}) {
    return super.requestGet<Record<string, unknown>>(`/api/admin/environments/${coid}`, {
      params: {
        environment: params.environment ?? 'staging',
        include_sync: params.include_sync ?? false,
        include_config: params.include_config ?? false,
      },
    })
  }

  create(payload: { data: Record<string, unknown>; environment?: string }) {
    return this.requestPost<Record<string, unknown>>('/api/admin/environments', {
      params: { environment: payload.environment ?? 'staging' },
      json: { data: payload.data },
    })
  }

  update(coid: string, payload: { updates: Record<string, unknown>; environment?: string }) {
    return this.requestPatch<Record<string, unknown>>(`/api/admin/environments/${coid}`, {
      params: { environment: payload.environment ?? 'staging' },
      json: { updates: payload.updates },
    })
  }

  delete(coid: string, params: { environment?: string } = {}) {
    return super.requestDelete<Record<string, unknown>>(`/api/admin/environments/${coid}`, {
      params: { environment: params.environment ?? 'staging' },
    })
  }

  copy(
    coid: string,
    payload: {
      source_environment?: string
      destination_environment?: string
      include_sync?: boolean
      overwrite_sync?: boolean
    } = {}
  ) {
    return this.requestPost<Record<string, unknown>>(`/api/admin/environments/${coid}/copy`, {
      json: dropNullish({
        source_environment: payload.source_environment ?? 'prod',
        destination_environment: payload.destination_environment ?? 'staging',
        include_sync: payload.include_sync ?? true,
        overwrite_sync: payload.overwrite_sync ?? true,
      }),
    })
  }
}
