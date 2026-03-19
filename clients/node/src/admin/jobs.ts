import { EndpointGroup } from '../base.js'

export class AdminJobsAPI extends EndpointGroup {
  run(payload: { coid: string; job_type: string; priority?: boolean }) {
    return this.requestPost<Record<string, unknown>>('/api/admin/jobs/run', {
      json: {
        coid: payload.coid,
        jobType: payload.job_type,
        priority: payload.priority ?? false,
      },
    })
  }

  list(coid: string, limit?: number) {
    return this.requestGet<Array<Record<string, unknown>>>(`/api/admin/jobs/${coid}`, {
      params: limit == null ? undefined : { limit },
    })
  }

  cancel(payload: { coid: string; dag_run_id: string }) {
    return this.requestPost<Record<string, unknown>>(
      `/api/admin/jobs/${payload.coid}/${payload.dag_run_id}/cancel`
    )
  }
}
