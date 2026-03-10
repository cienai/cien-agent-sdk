import { HTTPTransport } from '../transport'
import { PublicCompaniesAPI } from './companies'
import { PublicConfigAPI } from './config'
import { PublicPowerBIAPI } from './powerbi'
import { PublicUserCompanyPermissionsAPI } from './user-company-permissions'
import { PublicUsersAPI } from './users'
import { PublicVersionAPI } from './version'

export class PublicClient {
  readonly companies: PublicCompaniesAPI
  readonly config: PublicConfigAPI
  readonly powerbi: PublicPowerBIAPI
  readonly userCompanyPermissions: PublicUserCompanyPermissionsAPI
  readonly user_company_permissions: PublicUserCompanyPermissionsAPI
  readonly users: PublicUsersAPI
  readonly version: PublicVersionAPI

  constructor(transport: HTTPTransport) {
    this.companies = new PublicCompaniesAPI(transport)
    this.config = new PublicConfigAPI(transport)
    this.powerbi = new PublicPowerBIAPI(transport)
    this.userCompanyPermissions = new PublicUserCompanyPermissionsAPI(transport)
    this.user_company_permissions = this.userCompanyPermissions
    this.users = new PublicUsersAPI(transport)
    this.version = new PublicVersionAPI(transport)
  }
}
