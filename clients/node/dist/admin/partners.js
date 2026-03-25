import { EndpointGroup } from '../base.js';
import { dropNullish } from '../utils.js';
export class AdminPartnersAPI extends EndpointGroup {
    list(params = {}) {
        return super.requestGet('/api/admin/partners', {
            params: {
                include_deleted: params.include_deleted ?? false,
                include_inactive: params.include_inactive ?? true,
                show_all: params.show_all ?? false,
            },
        });
    }
    get(partnerId) {
        return super.requestGet(`/api/admin/partners/${partnerId}`);
    }
    create(payload) {
        return this.requestPost('/api/admin/partners', {
            json: dropNullish({ ...payload, is_active: payload.is_active ?? true }),
        });
    }
    update(partnerId, payload) {
        return this.requestPatch(`/api/admin/partners/${partnerId}`, {
            json: dropNullish(payload),
        });
    }
    delete(partnerId) {
        return super.requestDelete(`/api/admin/partners/${partnerId}`);
    }
}
