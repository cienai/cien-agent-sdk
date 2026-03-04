# Admin API Reference

Methods are available from `client.admin`.

## `companies`

- `list(partner_id=None, clerk_org_id=None, selected_columns=None, filters=None, order_by=None, limit=None, natural_query=None)`
  Lists companies with admin-scoped filters.
- `search(partner_id=None, clerk_org_id=None, selected_columns=None, filters=None, order_by=None, limit=None, natural_query=None)`
  Searches companies using a JSON payload.
- `get(coid, selected_columns=None)`
  Gets one company by COID.
- `lookup(company_id=None, company_name=None, selected_columns=None)`
  Looks up one company by ID or name.
- `update(company_id, updates, selected_columns=None)`
  Applies partial updates to a company.
- `delete(company_id)`
  Deletes a company by ID.

## `environments`

- `list(coid, include_sync=False)`
  Lists environment records for a company.
- `get(coid, environment="staging", include_sync=False)`
  Gets one environment record for a company.
- `create(data, environment="staging")`
  Creates an environment record.
- `update(coid, updates, environment="staging")`
  Applies partial updates to an environment record.
- `delete(coid, environment="staging")`
  Deletes an environment record.
- `copy(coid, source_environment="prod", destination_environment="staging", include_sync=True, overwrite_sync=True)`
  Copies environment data from source to destination.

## `partners`

- `list(include_deleted=False, include_inactive=True, show_all=False)`
  Lists partners with visibility flags.
- `get(partner_id)`
  Gets one partner by ID.
- `create(name, clerk_org_id=None, is_active=True)`
  Creates a partner.
- `update(partner_id, name=None, clerk_org_id=None, is_active=None, is_deleted=None)`
  Updates an existing partner.
- `delete(partner_id)`
  Deletes a partner.

## `powerbi`

- `get_workspace(workspace_id)`
  Gets one workspace.
- `list_reports(workspace_id)`
  Lists reports in a workspace.
- `list_report_pages(workspace_id, report_id)`
  Lists pages for a report.
- `list_datasets(workspace_id)`
  Lists datasets in a workspace.
- `generate_embed_token(workspace_id, report_id, dataset_ids=None, access_level="View", lifetime_minutes=None, allow_save_as=False)`
  Generates an embed token for report embedding.

## `sync`

- `list(coid=None, sync_token=None, sync_type=None, is_active=None)`
  Lists sync records filtered by company id and/or sync token. At least one of `coid` or `sync_token` is required.
- `get_by_sync_token(sync_token)`
  Gets one sync record by sync token via `/api/admin/sync/by-token/{sync_token}` (or `None` if not found).
- `get(sync_id)`
  Gets one sync record.
- `create(payload)`
  Creates a sync record.
- `update(sync_id, payload)`
  Updates an existing sync record.
- `delete(sync_id)`
  Deletes a sync record.

## `sync_source_definitions`

- `list(is_active=None)`
  Lists source definitions.
- `get(definition_id)`
  Gets one source definition by ID.
- `get_by_source_type(source_type)`
  Gets one source definition by source type.
- `create(display_name, source_type, meltano_plugin_name, env_prefix, required_settings=None, is_active=True)`
  Creates a source definition.
- `update(definition_id, payload)`
  Updates a source definition.
- `delete(definition_id)`
  Deletes a source definition.
