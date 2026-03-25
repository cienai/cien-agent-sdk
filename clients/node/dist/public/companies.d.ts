import { EndpointGroup } from '../base.js';
export declare class PublicCompaniesAPI extends EndpointGroup {
    list(params?: {
        selected_columns?: string[];
        filters?: string;
        order_by?: string;
        limit?: number;
        natural_query?: string;
    }): Promise<Record<string, unknown>[]>;
    search(payload?: {
        selected_columns?: string[];
        filters?: Record<string, unknown>;
        order_by?: string;
        limit?: number;
        natural_query?: string;
        clerk_org_id?: string;
    }): Promise<Record<string, unknown>[]>;
    get(coid: string, params?: {
        selected_columns?: string[];
    }): Promise<Record<string, unknown>>;
    lookup(params: {
        company_id?: string;
        company_name?: string;
        selected_columns?: string[];
    }): Promise<Record<string, unknown>>;
    update(companyId: string, payload: {
        updates: Record<string, unknown>;
        selected_columns?: string[];
    }): Promise<Record<string, unknown>>;
    delete(companyId: string): Promise<Record<string, unknown>>;
}
