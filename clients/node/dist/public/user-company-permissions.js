import { EndpointGroup } from '../base.js';
export class PublicUserCompanyPermissionsAPI extends EndpointGroup {
    listCompaniesForUser(params) {
        return this.requestGet(`/api/user-company-permissions/user/${params.email}/companies`, { params: { role: params.role ?? 'any' } });
    }
    listUsersForCompany(params) {
        return this.requestGet(`/api/user-company-permissions/company/${params.coid}/users`, { params: { role: params.role ?? 'any' } });
    }
    getCurrentUserPermissionForCompany(params) {
        return this.requestGet(`/api/user-company-permissions/company/${params.coid}/me`);
    }
    set(payload) {
        return this.requestPost('/api/user-company-permissions/set', {
            json: payload,
        });
    }
    remove(payload) {
        return this.requestPost('/api/user-company-permissions/remove', {
            json: payload,
        });
    }
}
