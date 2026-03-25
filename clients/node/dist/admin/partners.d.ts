import { EndpointGroup } from '../base.js';
export declare class AdminPartnersAPI extends EndpointGroup {
    list(params?: {
        include_deleted?: boolean;
        include_inactive?: boolean;
        show_all?: boolean;
    }): Promise<Record<string, unknown>[]>;
    get(partnerId: number): Promise<Record<string, unknown>>;
    create(payload: {
        name: string;
        clerk_org_id?: string;
        is_active?: boolean;
    }): Promise<Record<string, unknown>>;
    update(partnerId: number, payload: {
        name?: string;
        clerk_org_id?: string;
        clerk_org_slug?: string;
        max_allowed_memberships?: number;
        public_metadata?: Record<string, unknown>;
        private_metadata?: Record<string, unknown>;
        is_active?: boolean;
        is_deleted?: boolean;
    }): Promise<Record<string, unknown>>;
    delete(partnerId: number): Promise<Record<string, unknown>>;
}
