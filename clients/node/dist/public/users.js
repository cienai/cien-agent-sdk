import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class PublicUsersAPI extends EndpointGroup {
    issueToken(payload) {
        return this.requestPost('/api/users/token', { json: payload });
    }
    upsert(payload) {
        return this.requestPost('/api/users/upsert', {
            json: dropNullish({ ...payload, clerk_raw: payload.clerk_raw ?? {} }),
        });
    }
    invite(payload) {
        return this.requestPost('/api/users/invite', {
            json: dropNullish(payload),
        });
    }
    setCompanyPermission(payload) {
        return this.requestPost('/api/users/company-permissions/set', {
            json: payload,
        });
    }
    removeCompanyPermission(payload) {
        return this.requestPost('/api/users/company-permissions/remove', {
            json: payload,
        });
    }
    list(params = {}) {
        return this.requestGet('/api/users', {
            params: dropNullish({
                include_deleted: false,
                only_active: true,
                limit: 50,
                offset: 0,
                ...params,
            }),
        });
    }
    lookup(params) {
        return this.requestGet('/api/users/lookup', {
            params: dropNullish({ include_deleted: false, ...params }),
        });
    }
    whoAmI() {
        return this.requestGet('/whoami');
    }
}
