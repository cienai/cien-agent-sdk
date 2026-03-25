import { EndpointGroup } from '../base.js';
export declare class AdminSyncSourceDefinitionsAPI extends EndpointGroup {
    list(params?: {
        is_active?: boolean;
    }): Promise<Record<string, unknown>[]>;
    get(definitionId: number): Promise<Record<string, unknown>>;
    getBySourceType(sourceType: string): Promise<Record<string, unknown>>;
    create(payload: {
        display_name: string;
        source_type: string;
        meltano_plugin_name: string;
        env_prefix: string;
        required_settings?: unknown[];
        is_active?: boolean;
    }): Promise<Record<string, unknown>>;
    update(definitionId: number, payload: Record<string, unknown>): Promise<Record<string, unknown>>;
    delete(definitionId: number): Promise<void>;
}
