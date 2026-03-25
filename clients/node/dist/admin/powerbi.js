import { EndpointGroup } from '../base.js';
export class AdminPowerBIAPI extends EndpointGroup {
    getWorkspace(workspaceId) {
        return this.requestGet(`/api/admin/powerbi/workspaces/${workspaceId}`);
    }
    listReports(workspaceId) {
        return this.requestGet(`/api/admin/powerbi/workspaces/${workspaceId}/reports`);
    }
    listReportPages(workspaceId, reportId) {
        return this.requestGet(`/api/admin/powerbi/workspaces/${workspaceId}/reports/${reportId}/pages`);
    }
    listDatasets(workspaceId) {
        return this.requestGet(`/api/admin/powerbi/workspaces/${workspaceId}/datasets`);
    }
    generateEmbedToken(workspaceId, reportId, payload = {}) {
        return this.requestPost(`/api/admin/powerbi/workspaces/${workspaceId}/reports/${reportId}/embed-token`, {
            json: {
                dataset_ids: payload.dataset_ids,
                access_level: payload.access_level ?? 'View',
                lifetime_minutes: payload.lifetime_minutes,
                allow_save_as: payload.allow_save_as ?? false,
            },
        });
    }
}
