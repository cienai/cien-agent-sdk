import { EndpointGroup } from '../base'
import type { CompanyUserRoleFilter, PermissionRole, UserCompanyRoleFilter } from '../types'

export class PublicUserCompanyPermissionsAPI extends EndpointGroup {
  listCompaniesForUser(params: { email: string; role?: UserCompanyRoleFilter }) {
    return this.get<Array<Record<string, unknown>>>(
      `/api/user-company-permissions/user/${params.email}/companies`,
      { params: { role: params.role ?? 'any' } }
    )
  }

  listUsersForCompany(params: { coid: string; role?: CompanyUserRoleFilter }) {
    return this.get<Array<Record<string, unknown>>>(
      `/api/user-company-permissions/company/${params.coid}/users`,
      { params: { role: params.role ?? 'any' } }
    )
  }

  set(payload: { email: string; coid: string; permission_role: PermissionRole }) {
    return this.post<Record<string, unknown>>('/api/user-company-permissions/set', {
      json: payload,
    })
  }

  remove(payload: { email: string; coid: string }) {
    return this.post<Record<string, unknown>>('/api/user-company-permissions/remove', {
      json: payload,
    })
  }
}
