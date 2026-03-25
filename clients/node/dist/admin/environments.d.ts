import { EndpointGroup } from '../base.js';
export declare class AdminEnvironmentsAPI extends EndpointGroup {
    list(params: {
        coid: string;
        include_sync?: boolean;
        include_config?: boolean;
    }): Promise<Record<string, unknown>>;
    get(coid: string, params?: {
        environment?: string;
        include_sync?: boolean;
        include_config?: boolean;
    }): Promise<Record<string, unknown>>;
    create(payload: {
        data: Record<string, unknown>;
        environment?: string;
    }): Promise<Record<string, unknown>>;
    update(coid: string, payload: {
        updates: Record<string, unknown>;
        environment?: string;
    }): Promise<Record<string, unknown>>;
    delete(coid: string, params?: {
        environment?: string;
    }): Promise<Record<string, unknown>>;
    copy(coid: string, payload?: {
        source_environment?: string;
        destination_environment?: string;
        include_sync?: boolean;
        overwrite_sync?: boolean;
    }): Promise<Record<string, unknown>>;
}
