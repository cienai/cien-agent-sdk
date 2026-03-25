import { EndpointGroup } from '../base.js';
export class AdminJobsAPI extends EndpointGroup {
    run(payload) {
        return this.requestPost('/api/admin/jobs/run', {
            json: {
                coid: payload.coid,
                jobType: payload.job_type,
                priority: payload.priority ?? false,
            },
        });
    }
    list(coid, params) {
        return this.requestGet(`/api/admin/jobs/${coid}`, {
            params: params && (params.limit != null || params.offset != null)
                ? {
                    limit: params.limit,
                    offset: params.offset,
                }
                : undefined,
        });
    }
    cancel(payload) {
        return this.requestPost(`/api/admin/jobs/${payload.coid}/${payload.dag_run_id}/cancel`);
    }
}
