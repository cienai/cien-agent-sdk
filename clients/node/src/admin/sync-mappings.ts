import { EndpointGroup } from '../base.js'

export class AdminSyncMappingsAPI extends EndpointGroup {
  getMappingType(syncId: number) {
    return this.requestGet<Record<string, string>>(`/api/admin/sync-mappings/${syncId}/mapping-type`)
  }

  setMappingType(syncId: number, mappingType: string) {
    return this.requestPut<Record<string, string>>(`/api/admin/sync-mappings/${syncId}/mapping-type`, {
      json: { mapping_type: mappingType },
    })
  }

  getCrmEntities(syncId: number) {
    return this.requestGet<Record<string, string[]>>(`/api/admin/sync-mappings/${syncId}/crm-entities`)
  }

  getCienEntity(syncId: number, crmEntity: string) {
    return this.requestGet<Record<string, string | null>>(`/api/admin/sync-mappings/${syncId}/cien-entity`, {
      params: { crm_entity: crmEntity },
    })
  }

  getEntityOverrides(syncId: number) {
    return this.requestGet<Record<string, unknown>>(`/api/admin/sync-mappings/${syncId}/entity-overrides`)
  }

  setEntityOverrides(syncId: number, entityOverrides: unknown) {
    return this.requestPut<Record<string, unknown>>(`/api/admin/sync-mappings/${syncId}/entity-overrides`, {
      json: { entity_overrides: entityOverrides },
    })
  }

  getDefaultMapping(syncId: number, crmEntity: string) {
    return this.requestGet<Record<string, Array<Record<string, unknown>>>>(
      `/api/admin/sync-mappings/${syncId}/default-mapping`,
      {
        params: { crm_entity: crmEntity },
      }
    )
  }

  setDefaultMapping(syncId: number) {
    return this.requestPut<void>(`/api/admin/sync-mappings/${syncId}/default-mapping`)
  }

  getMappings(syncId: number) {
    return this.requestGet<Record<string, Record<string, Array<Record<string, unknown>>>>>(
      `/api/admin/sync-mappings/${syncId}/mappings`
    )
  }

  getMapping(syncId: number, crmEntity: string) {
    return this.requestGet<Array<Record<string, unknown>>>(
      `/api/admin/sync-mappings/${syncId}/mappings/${crmEntity}`
    )
  }

  setMapping(syncId: number, crmEntity: string, mappings: Array<Record<string, unknown>>) {
    return this.requestPut<Array<Record<string, unknown>>>(
      `/api/admin/sync-mappings/${syncId}/mappings/${crmEntity}`,
      {
        json: { mappings },
      }
    )
  }
}
