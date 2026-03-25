import { EndpointGroup } from '../base.js';
export class AdminMappingsAPI extends EndpointGroup {
    listCrmEntities(coid) {
        return this.requestGet(`/api/admin/mappings/${coid}/crm-entities`);
    }
    getCienEntity(coid, crmEntity) {
        return this.requestGet(`/api/admin/mappings/${coid}/cien-entity`, {
            params: { crm_entity: crmEntity },
        });
    }
    getCrmMappings(coid, crmEntity) {
        return this.requestGet(`/api/admin/mappings/${coid}/${crmEntity}`);
    }
    saveCrmMappings(coid, crmEntity, mappings) {
        return this.requestPut(`/api/admin/mappings/${coid}/${crmEntity}`, {
            json: { mappings },
        });
    }
}
