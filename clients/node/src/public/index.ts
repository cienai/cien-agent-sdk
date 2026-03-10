import { HTTPTransport } from '../transport.js'
import { PublicCompaniesAPI } from './companies.js'
import { PublicConfigAPI } from './config.js'
import { PublicPowerBIAPI } from './powerbi.js'
import { PublicUserCompanyPermissionsAPI } from './user-company-permissions.js'
import { PublicUsersAPI } from './users.js'
import { PublicVersionAPI } from './version.js'

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
