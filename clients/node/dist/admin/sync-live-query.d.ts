import { EndpointGroup } from '../base.js';
export declare class AdminSyncLiveQueryAPI extends EndpointGroup {
    describe(payload: {
        coid: string;
        crm_entity: string;
        column_names_only?: boolean;
    }): Promise<unknown>;
    query(payload: {
        coid: string;
        crm_entity: string;
        query: string;
        limit?: number | string;
    }): Promise<unknown>;
}
