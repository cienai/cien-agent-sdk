import { EndpointGroup } from '../base.js'

export class PublicPowerBIAPI extends EndpointGroup {
  listWorkspaces() {
    return this.get<Array<Record<string, unknown>>>('/api/powerbi/workspaces')
  }

  getWorkspace(workspaceId: string) {
    return this.get<Record<string, unknown>>(`/api/powerbi/workspaces/${workspaceId}`)
  }

  listReports(workspaceId: string) {
    return this.get<Array<Record<string, unknown>>>(`/api/powerbi/workspaces/${workspaceId}/reports`)
  }

  listReportPages(workspaceId: string, reportId: string) {
    return this.get<Array<Record<string, unknown>>>(
      `/api/powerbi/workspaces/${workspaceId}/reports/${reportId}/pages`
    )
  }

  listDatasets(workspaceId: string) {
    return this.get<Array<Record<string, unknown>>>(`/api/powerbi/workspaces/${workspaceId}/datasets`)
  }

  generateEmbedToken(
    workspaceId: string,
    reportId: string,
    payload: {
      dataset_ids?: string[]
      access_level?: string
      lifetime_minutes?: number
      allow_save_as?: boolean
    } = {}
  ) {
    return this.post<Record<string, unknown>>(
      `/api/powerbi/workspaces/${workspaceId}/reports/${reportId}/embed-token`,
      {
        json: {
          dataset_ids: payload.dataset_ids,
          access_level: payload.access_level ?? 'View',
          lifetime_minutes: payload.lifetime_minutes,
          allow_save_as: payload.allow_save_as ?? false,
        },
      }
    )
  }
}
