import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class PublicCompaniesAPI extends EndpointGroup {
    list(params = {}) {
        return super.requestGet('/api/companies', {
            params: dropNullish(params),
        });
    }
    search(payload = {}) {
        return this.requestPost('/api/companies/search', {
            json: dropNullish(payload),
        });
    }
    get(coid, params = {}) {
        return super.requestGet('/api/companies/companies', {
            params: dropNullish({ coid, ...params }),
        });
    }
    lookup(params) {
        return super.requestGet('/api/companies/lookup', {
            params: dropNullish(params),
        });
    }
    update(companyId, payload) {
        return this.requestPatch(`/api/companies/${companyId}`, {
            json: payload,
        });
    }
    delete(companyId) {
        return super.requestDelete(`/api/companies/${companyId}`);
    }
}
