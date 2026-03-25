import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class AdminCompaniesAPI extends EndpointGroup {
    list(params = {}) {
        return super.requestGet('/api/admin/companies', {
            params: dropNullish(params),
        });
    }
    search(payload = {}) {
        return this.requestPost('/api/admin/companies/search', {
            json: dropNullish(payload),
        });
    }
    create(payload) {
        return this.requestPost('/api/admin/companies', { json: payload });
    }
    get(coid, params = {}) {
        return super.requestGet('/api/admin/companies/companies', {
            params: dropNullish({ coid, ...params }),
        });
    }
    lookup(params) {
        return super.requestGet('/api/admin/companies/lookup', {
            params: dropNullish(params),
        });
    }
    update(companyId, payload) {
        return this.requestPatch(`/api/admin/companies/${companyId}`, {
            json: payload,
        });
    }
    delete(companyId) {
        return super.requestDelete(`/api/admin/companies/${companyId}`);
    }
}
