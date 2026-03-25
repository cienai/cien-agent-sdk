import { EndpointGroup } from '../base.js'
import { dropNullish } from '../utils.js'

export class AdminJobDataAPI extends EndpointGroup {
  upload(payload: {
    coid: string
    upload_type: 'hr_file' | 'aliasing' | 'groups' | 'opp_stages'
    file: File
  }) {
    const formData = new FormData()
    formData.set('upload_type', payload.upload_type)
    formData.set('file', payload.file)

    return this.requestPost<Record<string, unknown>>(
      `/api/admin/job-data/${payload.coid}/upload`,
      {
        body: formData,
      }
    )
  }

  get(coid: string) {
    return super.requestGet<Record<string, unknown>>(`/api/admin/job-data/${coid}`)
  }

  download(payload: { coid: string; key: string }) {
    return super.requestGet<string>(`/api/admin/job-data/${payload.coid}/download`, {
      params: dropNullish({
        key: payload.key,
      }),
    })
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

  explore(payload: {
    coid: string
    prefix?: string
    limit?: number
    recursive?: boolean
  }) {
    return super.requestGet<Record<string, unknown>>(`/api/admin/job-data/${payload.coid}/explore`, {
      params: dropNullish({
        prefix: payload.prefix,
        limit: payload.limit,
        recursive: payload.recursive,
      }),
    })
  }

  sizes(payload: {
    coid: string
    prefix?: string
    include_container_total?: boolean
  }) {
    return super.requestGet<Record<string, unknown>>(`/api/admin/job-data/${payload.coid}/sizes`, {
      params: dropNullish({
        prefix: payload.prefix,
        include_container_total: payload.include_container_total,
      }),
    })
  }
}
