import { EndpointGroup } from '../base'

export class PublicVersionAPI extends EndpointGroup {
  get() {
    return super.requestGet<Record<string, unknown>>('/version')
  }
}
