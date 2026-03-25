import { EndpointGroup } from '../base.js';
export declare class AdminPowerBIAPI extends EndpointGroup {
    getWorkspace(workspaceId: string): Promise<Record<string, unknown>>;
    listReports(workspaceId: string): Promise<Record<string, unknown>[]>;
    listReportPages(workspaceId: string, reportId: string): Promise<Record<string, unknown>[]>;
    listDatasets(workspaceId: string): Promise<Record<string, unknown>[]>;
    generateEmbedToken(workspaceId: string, reportId: string, payload?: {
        dataset_ids?: string[];
        access_level?: string;
        lifetime_minutes?: number;
        allow_save_as?: boolean;
    }): Promise<Record<string, unknown>>;
}
