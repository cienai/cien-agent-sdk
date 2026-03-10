import { EndpointGroup } from '../base'

export class PublicVersionAPI extends EndpointGroup {
  get() {
    return super.get<Record<string, unknown>>('/version')
  }
}
