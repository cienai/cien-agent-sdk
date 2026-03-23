import { EndpointGroup } from '../base.js'
import { dropNullish } from '../utils.js'

export class AdminJobDataAPI extends EndpointGroup {
  get(coid: string) {
    return super.requestGet<Record<string, unknown>>(`/api/admin/job-data/${coid}`)
  }

  create(coid: string) {
    return this.requestPost<Record<string, unknown>>(`/api/admin/job-data/${coid}/create`)
  }

  save(payload: { coid: string; value: unknown; config_type?: string }) {
    return this.requestPost<Record<string, unknown>>(`/api/admin/job-data/${payload.coid}`, {
      json: dropNullish({
        value: payload.value,
        type: payload.config_type,
      }),
    })
  }

  refresh(payload: { coid: string; region: string }) {
    return this.requestPost<Record<string, unknown>>(`/api/admin/job-data/${payload.coid}/refresh`, {
      json: dropNullish({
        region: payload.region,
      }),
    })
  }
}
