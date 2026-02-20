# Public API Reference

Methods are available from `client.public`.

## `version`

- `get()`
  Returns service version metadata.

## `users`

- `issue_token(username, password)`
  Exchanges service-account credentials for a token.
- `upsert(clerk_user_id, clerk_org_id, ...)`
  Creates or updates a user from identity-provider attributes.
- `invite(identifier, partner_id=None)`
  Sends a user invitation.
- `set_company_permission(email, coid, permissions)`
  Sets a user's permission string for a company.
- `remove_company_permission(email, coid)`
  Removes a user's company permission.
- `list(clerk_org_id=None, partner_id=None, search=None, include_deleted=False, only_active=True, limit=50, offset=0)`
  Lists users with filters and pagination.
- `lookup(clerk_user_id=None, clerk_org_id=None, email=None, include_deleted=False)`
  Looks up one user by external ID or email.
- `whoami()`
  Returns the authenticated user.

## `companies`

- `list(selected_columns=None, filters=None, order_by=None, limit=None, natural_query=None)`
  Lists companies using query-string filters.
- `search(selected_columns=None, filters=None, order_by=None, limit=None, natural_query=None)`
  Searches companies using a structured JSON payload.
- `get(coid, selected_columns=None)`
  Gets one company by COID.
- `lookup(company_id=None, company_name=None, selected_columns=None)`
  Looks up one company by company ID or company name.
- `update(company_id, updates, selected_columns=None)`
  Applies partial updates to a company.
- `delete(company_id)`
  Deletes a company by ID.

## `config`

- `list(coid, key=None, level=None, convert_dtypes=False)`
  Lists config rows for a company.
- `get(coid, key, convert_dtypes=False)`
  Gets one config value.
- `save(coid, key, config_type, value=None)`
  Creates or updates one config value.
- `delete(coid, key)`
  Deletes one config value.

## `powerbi`

- `list_workspaces()`
  Lists accessible workspaces.
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

## `user_company_permissions`

- `list_companies_for_user(email, role="any")`
  Lists companies a user can access.
- `list_users_for_company(coid, role="any")`
  Lists users with access to a company.
- `set(email, coid, permission_role)`
  Sets a user's role (`view`, `manage`, `owner`) for a company.
- `remove(email, coid)`
  Removes a user's company permission.
