import { EndpointGroup } from '../base.js';
export declare class PublicConfigAPI extends EndpointGroup {
    list(params: {
        coid: string;
        key?: string;
        level?: string;
        convert_dtypes?: boolean;
    }): Promise<Record<string, unknown>[]>;
    get(params: {
        coid: string;
        key: string;
        convert_dtypes?: boolean;
    }): Promise<Record<string, unknown>>;
    save(payload: {
        coid: string;
        key: string;
        config_type: string;
        value?: unknown;
    }): Promise<Record<string, unknown>>;
    update(payload: {
        coid: string;
        config: Array<Record<string, unknown>>;
    }): Promise<Record<string, unknown>[]>;
    delete(params: {
        coid: string;
        key: string;
    }): Promise<void>;
}
