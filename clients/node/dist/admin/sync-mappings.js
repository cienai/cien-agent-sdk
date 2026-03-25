import { EndpointGroup } from '../base.js';
export class AdminSyncMappingsAPI extends EndpointGroup {
    getMappingType(syncId) {
        return this.requestGet(`/api/admin/sync-mappings/${syncId}/mapping-type`);
    }
    setMappingType(syncId, mappingType) {
        return this.requestPut(`/api/admin/sync-mappings/${syncId}/mapping-type`, {
            json: { mapping_type: mappingType },
        });
    }
    getCrmEntities(syncId) {
        return this.requestGet(`/api/admin/sync-mappings/${syncId}/crm-entities`);
    }
    getCienEntity(syncId, crmEntity) {
        return this.requestGet(`/api/admin/sync-mappings/${syncId}/cien-entity`, {
            params: { crm_entity: crmEntity },
        });
    }
    getCienEntities(syncId) {
        return this.requestGet(`/api/admin/sync-mappings/${syncId}/cien-entities`);
    }
    getEntityOverrides(syncId) {
        return this.requestGet(`/api/admin/sync-mappings/${syncId}/entity-overrides`);
    }
    setEntityOverrides(syncId, entityOverrides) {
        return this.requestPut(`/api/admin/sync-mappings/${syncId}/entity-overrides`, {
            json: { entity_overrides: entityOverrides },
        });
    }
    getDefaultMapping(syncId, crmEntity) {
        return this.requestGet(`/api/admin/sync-mappings/${syncId}/default-mapping`, {
            params: { crm_entity: crmEntity },
        });
    }
    setDefaultMapping(syncId) {
        return this.requestPut(`/api/admin/sync-mappings/${syncId}/default-mapping`);
    }
    getMappings(syncId) {
        return this.requestGet(`/api/admin/sync-mappings/${syncId}/mappings`);
    }
    getMapping(syncId, crmEntity) {
        return this.requestGet(`/api/admin/sync-mappings/${syncId}/mappings/${crmEntity}`);
    }
    setMapping(syncId, crmEntity, mappings) {
        return this.requestPut(`/api/admin/sync-mappings/${syncId}/mappings/${crmEntity}`, {
            json: { mappings },
        });
    }
    patchMappingItem(syncId, crmEntity, mapping) {
        return this.requestPatch(`/api/admin/sync-mappings/${syncId}/mappings/${crmEntity}`, {
            json: { mapping },
        });
    }
}
