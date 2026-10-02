import { test } from 'node:test'
import assert from 'node:assert/strict'
import { AdminSyncLiveQueryAPI } from '../dist/admin/sync-live-query.js'

test('describe and query carry the selected sync; legacy callers omit it', async () => {
  const calls = []
  const api = new AdminSyncLiveQueryAPI({ request: async (...args) => { calls.push(args); return [] } })
  await api.describe({ coid: 'A', sync_id: 708, crm_entity: 'Account' })
  await api.query({ coid: 'A', sync_id: 708, crm_entity: 'Account', query: 'SELECT * FROM Account', limit: 1 })
  assert.equal(calls[0][2].json.sync_id, 708)
  assert.equal(calls[1][2].json.sync_id, 708)
  assert.equal(calls[1][2].json.limit, 1)
  await api.describe({ coid: 'A', crm_entity: 'Account' })
  assert.equal(Object.hasOwn(calls[2][2].json, 'sync_id'), false)
})
