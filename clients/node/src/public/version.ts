import { EndpointGroup } from '../base.js'

export class PublicVersionAPI extends EndpointGroup {
  get() {
    return super.get<Record<string, unknown>>('/version')
  }
}
