# Table UI and Interaction Guidelines

These rules apply to all data tables across the application (Admin, Realtor, Client views):

1) Actions column
- Collapse all row actions into a single “Actions” dropdown per row.
- Use a small outline secondary button labeled “Actions” with a dropdown menu.
- Menu items can be standard links (hx_get) or HTMX posts (hx_post) to the same route handlers.
- Destructive items (Reject/Delete) MUST include a confirmation prompt (hx_confirm).

2) Responsiveness and horizontal scroll
- Wrap every <Table> in a container with class `table-responsive` to enable horizontal scrolling on smaller screens.
- Keep table classes `table table-striped table-hover` for readability.

3) Status badges
- Map domain status values to badge colors consistently:
  - approved, paid, success -> badge bg-success
  - pending, in_progress, processing -> badge bg-warning
  - rejected, failed, cancelled, error -> badge bg-danger
  - anything else -> badge bg-secondary
- Always render status cells with a <Span> that uses the mapped badge class and a title-cased label.

4) Pagination
- Default page size is 10 rows. Do not render more than 10 rows per page.
- Implement simple pagination controls below each table: Previous | Page X of Y | Next
- Controls should navigate using hx_get to the same endpoint with a `?page=` query param and target `#main-content`.
- Disable the corresponding control when at the first or last page.

5) Fragments and HTMX
- Tables should be renderable both in full page layouts and as HTMX fragments (honor HX-Request header in route handlers).
- Pagination links and actions should update `#main-content` via HTMX swaps.

6) Accessibility and consistency
- Use clear button labels in menus (e.g., View, Approve, Reject, Edit, Delete).
- Keep numerical and currency columns formatted (e.g., ₦1,234.56).
- Maintain column order: identifiers, key descriptors, amounts, statuses, timestamps, actions.

7) Performance
- Fetch full result sets server-side but only render the current page (slice rows in memory or via query).
- Consider indexing frequently filtered columns (status, created_at) in the database when scale increases.
