import { EndpointGroup } from '../base.js';
export declare class AdminMappingsAPI extends EndpointGroup {
    listCrmEntities(coid: string): Promise<Record<string, string[]>>;
    getCienEntity(coid: string, crmEntity: string): Promise<Record<string, string | null>>;
    getCrmMappings(coid: string, crmEntity: string): Promise<Record<string, unknown>[]>;
    saveCrmMappings(coid: string, crmEntity: string, mappings: Array<Record<string, unknown>>): Promise<Record<string, unknown>[]>;
}
