import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class AdminJobDataAPI extends EndpointGroup {
    upload(payload) {
        const formData = new FormData();
        formData.set('upload_type', payload.upload_type);
        formData.set('file', payload.file);
        return this.requestPost(`/api/admin/job-data/${payload.coid}/upload`, {
            body: formData,
        });
    }
    get(coid) {
        return super.requestGet(`/api/admin/job-data/${coid}`);
    }
    download(payload) {
        return super.requestGet(`/api/admin/job-data/${payload.coid}/download`, {
            params: dropNullish({
                key: payload.key,
            }),
        });
    }
    create(coid) {
        return this.requestPost(`/api/admin/job-data/${coid}/create`);
    }
    save(payload) {
        return this.requestPost(`/api/admin/job-data/${payload.coid}`, {
            json: dropNullish({
                value: payload.value,
                type: payload.config_type,
            }),
        });
    }
    refresh(payload) {
        return this.requestPost(`/api/admin/job-data/${payload.coid}/refresh`, {
            json: dropNullish({
                region: payload.region,
            }),
        });
    }
    explore(payload) {
        return super.requestGet(`/api/admin/job-data/${payload.coid}/explore`, {
            params: dropNullish({
                prefix: payload.prefix,
                limit: payload.limit,
                recursive: payload.recursive,
            }),
        });
    }
    sizes(payload) {
        return super.requestGet(`/api/admin/job-data/${payload.coid}/sizes`, {
            params: dropNullish({
                prefix: payload.prefix,
                include_container_total: payload.include_container_total,
            }),
        });
    }
}
