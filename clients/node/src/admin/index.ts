import { HTTPTransport } from '../transport'
import { AdminCompaniesAPI } from './companies'
import { AdminCrmAPI } from './crm'
import { AdminEnvironmentsAPI } from './environments'
import { AdminMappingsAPI } from './mappings'
import { AdminPartnersAPI } from './partners'
import { AdminPowerBIAPI } from './powerbi'
import { AdminSyncAPI } from './sync'
import { AdminSyncSourceDefinitionsAPI } from './sync-source-definitions'

export class AdminClient {
  readonly companies: AdminCompaniesAPI
  readonly crm: AdminCrmAPI
  readonly environments: AdminEnvironmentsAPI
  readonly mappings: AdminMappingsAPI
  readonly partners: AdminPartnersAPI
  readonly powerbi: AdminPowerBIAPI
  readonly sync: AdminSyncAPI
  readonly syncSourceDefinitions: AdminSyncSourceDefinitionsAPI
  readonly sync_source_definitions: AdminSyncSourceDefinitionsAPI

  constructor(transport: HTTPTransport) {
    this.companies = new AdminCompaniesAPI(transport)
    this.crm = new AdminCrmAPI(transport)
    this.environments = new AdminEnvironmentsAPI(transport)
    this.mappings = new AdminMappingsAPI(transport)
    this.partners = new AdminPartnersAPI(transport)
    this.powerbi = new AdminPowerBIAPI(transport)
    this.sync = new AdminSyncAPI(transport)
    this.syncSourceDefinitions = new AdminSyncSourceDefinitionsAPI(transport)
    this.sync_source_definitions = this.syncSourceDefinitions
  }
}
