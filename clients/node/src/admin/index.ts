import { HTTPTransport } from '../transport.js'
import { AdminCompaniesAPI } from './companies.js'
import { AdminCrmAPI } from './crm.js'
import { AdminEnvironmentsAPI } from './environments.js'
import { AdminMappingsAPI } from './mappings.js'
import { AdminPartnersAPI } from './partners.js'
import { AdminPowerBIAPI } from './powerbi.js'
import { AdminSyncAPI } from './sync.js'
import { AdminSyncMappingsAPI } from './sync-mappings.js'
import { AdminSyncSourceDefinitionsAPI } from './sync-source-definitions.js'

export class AdminClient {
  readonly companies: AdminCompaniesAPI
  readonly crm: AdminCrmAPI
  readonly environments: AdminEnvironmentsAPI
  readonly mappings: AdminMappingsAPI
  readonly partners: AdminPartnersAPI
  readonly powerbi: AdminPowerBIAPI
  readonly sync: AdminSyncAPI
  readonly syncMappings: AdminSyncMappingsAPI
  readonly sync_mappings: AdminSyncMappingsAPI
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
    this.syncMappings = new AdminSyncMappingsAPI(transport)
    this.sync_mappings = this.syncMappings
    this.syncSourceDefinitions = new AdminSyncSourceDefinitionsAPI(transport)
    this.sync_source_definitions = this.syncSourceDefinitions
  }
}
