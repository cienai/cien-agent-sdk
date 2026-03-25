import { EndpointGroup } from '../base.js'
import type { CompanyUserRoleFilter, PermissionRole, UserCompanyRoleFilter } from '../types.js'

export class PublicUserCompanyPermissionsAPI extends EndpointGroup {
  listCompaniesForUser(params: { email: string; role?: UserCompanyRoleFilter }) {
    return this.requestGet<Array<Record<string, unknown>>>(
      `/api/user-company-permissions/user/${params.email}/companies`,
      { params: { role: params.role ?? 'any' } }
    )
  }

  listUsersForCompany(params: { coid: string; role?: CompanyUserRoleFilter }) {
    return this.requestGet<Array<Record<string, unknown>>>(
      `/api/user-company-permissions/company/${params.coid}/users`,
      { params: { role: params.role ?? 'any' } }
    )
  }

  getCurrentUserPermissionForCompany(params: { coid: string }) {
    return this.requestGet<Record<string, unknown>>(
      `/api/user-company-permissions/company/${params.coid}/me`
    )
  }

  set(payload: { email: string; coid: string; permission_role: PermissionRole }) {
    return this.requestPost<Record<string, unknown>>('/api/user-company-permissions/set', {
      json: payload,
    })
  }

  remove(payload: { email: string; coid: string }) {
    return this.requestPost<Record<string, unknown>>('/api/user-company-permissions/remove', {
      json: payload,
    })
  }
}
