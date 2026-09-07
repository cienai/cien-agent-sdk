import { EndpointGroup } from '../base.js'

export class AdminJobsAPI extends EndpointGroup {
  run(payload: { coid: string; job_type: string; processing_mode?: string; priority?: boolean }) {
    return this.requestPost<Record<string, unknown>>('/api/admin/jobs/run', {
      json: {
        coid: payload.coid,
        jobType: payload.job_type,
        ...(payload.processing_mode ? { processingMode: payload.processing_mode } : {}),
        priority: payload.priority ?? false,
      },
    })
  }

  list(
    coid: string,
    params?: { limit?: number; offset?: number }
  ) {
    return this.requestGet<Record<string, unknown>>(`/api/admin/jobs/${coid}`, {
      params:
        params && (params.limit != null || params.offset != null)
          ? {
              limit: params.limit,
              offset: params.offset,
            }
          : undefined,
    })
  }

  cancel(payload: { coid: string; dag_run_id: string }) {
    return this.requestPost<Record<string, unknown>>(
      `/api/admin/jobs/${payload.coid}/${payload.dag_run_id}/cancel`
    )
  }
}
