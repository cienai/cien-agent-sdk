import { EndpointGroup } from '../base'
import { dropNullish } from '../utils'

export class AdminSyncSourceDefinitionsAPI extends EndpointGroup {
  list(params: { is_active?: boolean } = {}) {
    return super.get<Array<Record<string, unknown>>>('/api/admin/sync-source-definitions', {
      params: dropNullish(params),
    })
  }

  get(definitionId: number) {
    return super.get<Record<string, unknown>>(`/api/admin/sync-source-definitions/${definitionId}`)
  }

  getBySourceType(sourceType: string) {
    return super.get<Record<string, unknown>>(
      `/api/admin/sync-source-definitions/source-type/${sourceType}`
    )
  }

  create(payload: {
    display_name: string
    source_type: string
    meltano_plugin_name: string
    env_prefix: string
    required_settings?: unknown[]
    is_active?: boolean
  }) {
    return this.post<Record<string, unknown>>('/api/admin/sync-source-definitions', {
      json: {
        ...payload,
        required_settings: payload.required_settings ?? [],
        is_active: payload.is_active ?? true,
      },
    })
  }

  update(definitionId: number, payload: Record<string, unknown>) {
    return this.patch<Record<string, unknown>>(
      `/api/admin/sync-source-definitions/${definitionId}`,
      { json: payload }
    )
  }

  async delete(definitionId: number) {
    await super.delete(`/api/admin/sync-source-definitions/${definitionId}`)
  }
}
