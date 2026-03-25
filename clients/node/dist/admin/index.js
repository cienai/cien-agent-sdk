import { AdminCompaniesAPI } from './companies.js';
import { AdminCrmAPI } from './crm.js';
import { AdminEnvironmentsAPI } from './environments.js';
import { AdminJobsAPI } from './jobs.js';
import { AdminJobDataAPI } from './job-data.js';
import { AdminMappingsAPI } from './mappings.js';
import { AdminPartnersAPI } from './partners.js';
import { AdminPowerBIAPI } from './powerbi.js';
import { AdminSyncAPI } from './sync.js';
import { AdminSyncLiveQueryAPI } from './sync-live-query.js';
import { AdminSyncMappingsAPI } from './sync-mappings.js';
import { AdminSyncSourceDefinitionsAPI } from './sync-source-definitions.js';
export class AdminClient {
    companies;
    crm;
    environments;
    jobs;
    jobData;
    job_data;
    mappings;
    partners;
    powerbi;
    sync;
    syncLiveQuery;
    sync_live_query;
    syncMappings;
    sync_mappings;
    syncSourceDefinitions;
    sync_source_definitions;
    constructor(transport) {
        this.companies = new AdminCompaniesAPI(transport);
        this.crm = new AdminCrmAPI(transport);
        this.environments = new AdminEnvironmentsAPI(transport);
        this.jobs = new AdminJobsAPI(transport);
        this.jobData = new AdminJobDataAPI(transport);
        this.job_data = this.jobData;
        this.mappings = new AdminMappingsAPI(transport);
        this.partners = new AdminPartnersAPI(transport);
        this.powerbi = new AdminPowerBIAPI(transport);
        this.sync = new AdminSyncAPI(transport);
        this.syncLiveQuery = new AdminSyncLiveQueryAPI(transport);
        this.sync_live_query = this.syncLiveQuery;
        this.syncMappings = new AdminSyncMappingsAPI(transport);
        this.sync_mappings = this.syncMappings;
        this.syncSourceDefinitions = new AdminSyncSourceDefinitionsAPI(transport);
        this.sync_source_definitions = this.syncSourceDefinitions;
    }
}
