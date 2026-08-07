import { EndpointGroup } from '../base.js';
export declare class AdminJobsAPI extends EndpointGroup {
    run(payload: {
        coid: string;
        job_type: string;
        processing_mode?: string;
        priority?: boolean;
    }): Promise<Record<string, unknown>>;
    list(coid: string, params?: {
        limit?: number;
        offset?: number;
    }): Promise<Record<string, unknown>>;
    cancel(payload: {
        coid: string;
        dag_run_id: string;
    }): Promise<Record<string, unknown>>;
}
