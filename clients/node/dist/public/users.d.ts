import { EndpointGroup } from '../base.js';
export declare class PublicUsersAPI extends EndpointGroup {
    issueToken(payload: {
        username: string;
        password: string;
    }): Promise<Record<string, unknown>>;
    upsert(payload: {
        clerk_user_id: string;
        clerk_org_id: string;
        clerk_session_id?: string;
        email?: string;
        display_name?: string;
        given_name?: string;
        surname?: string;
        clerk_raw?: Record<string, unknown>;
        partner_id?: number;
    }): Promise<Record<string, unknown>>;
    invite(payload: {
        identifier: string;
        partner_id?: number;
    }): Promise<Record<string, unknown>>;
    setCompanyPermission(payload: {
        email: string;
        coid: string;
        permissions: string;
    }): Promise<Record<string, unknown>>;
    removeCompanyPermission(payload: {
        email: string;
        coid: string;
    }): Promise<Record<string, unknown>>;
    list(params?: {
        clerk_org_id?: string;
        partner_id?: number;
        search?: string;
        include_deleted?: boolean;
        only_active?: boolean;
        limit?: number;
        offset?: number;
    }): Promise<Record<string, unknown>[]>;
    lookup(params: {
        clerk_user_id?: string;
        clerk_org_id?: string;
        email?: string;
        include_deleted?: boolean;
    }): Promise<Record<string, unknown>>;
    whoAmI(): Promise<Record<string, unknown>>;
}
