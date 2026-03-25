import { EndpointGroup } from '../base.js';
export interface ResetSyncResponse {
    message: string;
    coid: string;
    entity: string;
    status_cleared: boolean;
    deleted_files: string[];
    errors: string[];
}
export declare class AdminSyncAPI extends EndpointGroup {
    list(params: {
        coid?: string;
        sync_token?: string;
        sync_type?: string;
        is_active?: boolean;
    }): Promise<Record<string, unknown>[]>;
    getBySyncToken(syncToken: string): Promise<Record<string, unknown> | null>;
    get(syncId: number): Promise<Record<string, unknown>>;
    create(payload: Record<string, unknown>): Promise<Record<string, unknown>>;
    update(syncId: number, payload: Record<string, unknown>): Promise<Record<string, unknown>>;
    delete(syncId: number): Promise<void>;
    reset(payload: {
        sync_id: number;
        crm_entity: string;
        reset_delta?: boolean;
    }): Promise<ResetSyncResponse>;
}
