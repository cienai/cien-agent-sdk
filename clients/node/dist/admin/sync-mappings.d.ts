import { EndpointGroup } from '../base.js';
export declare class AdminSyncMappingsAPI extends EndpointGroup {
    getMappingType(syncId: number): Promise<Record<string, string>>;
    setMappingType(syncId: number, mappingType: string): Promise<Record<string, string>>;
    getCrmEntities(syncId: number): Promise<Record<string, string[]>>;
    getCienEntity(syncId: number, crmEntity: string): Promise<Record<string, string | null>>;
    getCienEntities(syncId: number): Promise<Record<string, Record<string, string | null>>>;
    getEntityOverrides(syncId: number): Promise<Record<string, unknown>>;
    setEntityOverrides(syncId: number, entityOverrides: unknown): Promise<Record<string, unknown>>;
    getDefaultMapping(syncId: number, crmEntity: string): Promise<Record<string, Record<string, unknown>[]>>;
    setDefaultMapping(syncId: number): Promise<void>;
    getMappings(syncId: number): Promise<Record<string, Record<string, Record<string, unknown>[]>>>;
    getMapping(syncId: number, crmEntity: string): Promise<Record<string, unknown>[]>;
    setMapping(syncId: number, crmEntity: string, mappings: Array<Record<string, unknown>>): Promise<Record<string, unknown>[]>;
    patchMappingItem(syncId: number, crmEntity: string, mapping: Record<string, unknown>): Promise<Record<string, unknown>[]>;
}
