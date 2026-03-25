import { EndpointGroup } from '../base.js';
export declare class AdminCrmAPI extends EndpointGroup {
    describe(payload: {
        coid: string;
        table: string;
        column_names_only?: boolean;
    }): Promise<unknown>;
    query(payload: {
        coid: string;
        table: string;
        query: string;
        limit?: number;
    }): Promise<unknown>;
}
