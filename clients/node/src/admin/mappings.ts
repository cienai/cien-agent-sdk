import { EndpointGroup } from '../base'

export class AdminMappingsAPI extends EndpointGroup {
  listCrmEntities(coid: string) {
    return this.get<Record<string, string[]>>(`/api/admin/mappings/${coid}/crm-entities`)
  }

  getCienEntity(coid: string, crmEntity: string) {
    return this.get<Record<string, string | null>>(`/api/admin/mappings/${coid}/cien-entity`, {
      params: { crm_entity: crmEntity },
    })
  }

  getCrmMappings(coid: string, crmEntity: string) {
    return this.get<Array<Record<string, unknown>>>(`/api/admin/mappings/${coid}/${crmEntity}`)
  }

  saveCrmMappings(coid: string, crmEntity: string, mappings: Array<Record<string, unknown>>) {
    return this.put<Array<Record<string, unknown>>>(`/api/admin/mappings/${coid}/${crmEntity}`, {
      json: { mappings },
    })
  }
}
