import { EndpointGroup } from '../base.js';
export declare class AdminJobDataAPI extends EndpointGroup {
    upload(payload: {
        coid: string;
        upload_type: 'hr_file' | 'aliasing' | 'groups' | 'opp_stages';
        file: File;
    }): Promise<Record<string, unknown>>;
    get(coid: string): Promise<Record<string, unknown>>;
    download(payload: {
        coid: string;
        key: string;
    }): Promise<string>;
    create(coid: string): Promise<Record<string, unknown>>;
    save(payload: {
        coid: string;
        value: unknown;
        config_type?: string;
    }): Promise<Record<string, unknown>>;
    refresh(payload: {
        coid: string;
        region: string;
    }): Promise<Record<string, unknown>>;
    explore(payload: {
        coid: string;
        prefix?: string;
        limit?: number;
        recursive?: boolean;
    }): Promise<Record<string, unknown>>;
    sizes(payload: {
        coid: string;
        prefix?: string;
        include_container_total?: boolean;
    }): Promise<Record<string, unknown>>;
}
