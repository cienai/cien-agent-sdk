import { EndpointGroup } from '../base.js';
export declare class PublicVersionAPI extends EndpointGroup {
    get(): Promise<Record<string, unknown>>;
}
