import { EndpointGroup } from '../base.js'
import { dropNullish } from '../utils.js'

export class PublicConfigAPI extends EndpointGroup {
  list(params: {
    coid: string
    key?: string
    level?: string
    convert_dtypes?: boolean
  }) {
    return super.requestGet<Array<Record<string, unknown>>>('/api/config', {
      params: dropNullish(params),
    })
  }

  get(params: { coid: string; key: string; convert_dtypes?: boolean }) {
    return super.requestGet<Record<string, unknown>>(`/api/config/${params.coid}/${params.key}`, {
      params: { convert_dtypes: params.convert_dtypes ?? false },
    })
  }

  save(payload: { coid: string; key: string; config_type: string; value?: unknown }) {
    return this.requestPost<Record<string, unknown>>(`/api/config/${payload.coid}`, {
      json: { key: payload.key, type: payload.config_type, value: payload.value },
    })
  }

  update(payload: { coid: string; config: Array<Record<string, unknown>> }) {
    return this.requestPut<Array<Record<string, unknown>>>(`/api/config/${payload.coid}`, {
      json: { config: payload.config },
    })
  }

  async delete(params: { coid: string; key: string }) {
    await super.requestDelete(`/api/config/${params.coid}/${params.key}`)
  }
}
