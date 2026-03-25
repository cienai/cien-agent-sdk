import { EndpointGroup } from '../base.js';
import type { CompanyUserRoleFilter, PermissionRole, UserCompanyRoleFilter } from '../types.js';
export declare class PublicUserCompanyPermissionsAPI extends EndpointGroup {
    listCompaniesForUser(params: {
        email: string;
        role?: UserCompanyRoleFilter;
    }): Promise<Record<string, unknown>[]>;
    listUsersForCompany(params: {
        coid: string;
        role?: CompanyUserRoleFilter;
    }): Promise<Record<string, unknown>[]>;
    getCurrentUserPermissionForCompany(params: {
        coid: string;
    }): Promise<Record<string, unknown>>;
    set(payload: {
        email: string;
        coid: string;
        permission_role: PermissionRole;
    }): Promise<Record<string, unknown>>;
    remove(payload: {
        email: string;
        coid: string;
    }): Promise<Record<string, unknown>>;
}
