# Tasks: Real Estate Investment Platform

**Input**: Design documents from `specs/001-description-a-real/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `backend/src/`, `frontend/src/`

- [x] T001 Create project structure with `main.py` for `python-fasthtml` app initialization.
- [x] T002 [P] Initialize `python-fasthtml` app in `main.py` with `sqlite` database.
- [x] T003 [P] Set up `pytest` in `backend/` for testing.
- [x] T004 [P] Configure linting and formatting tools (e.g., ruff, black) in `backend/`.

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T005 [P] Contract test for `GET /users` in `backend/tests/contract/test_users.py`.
- [x] T006 [P] Contract test for `POST /users` in `backend/tests/contract/test_users.py`.
- [x] T007 [P] Contract test for `GET /properties` in `backend/tests/contract/test_properties.py`.
- [x] T008 [P] Contract test for `POST /properties` in `backend/tests/contract/test_properties.py`.
- [x] T009 [P] Contract test for `POST /enquiries` in `backend/tests/contract/test_enquiries.py`.
- [x] T010 [P] Integration test for Client workflow in `backend/tests/integration/test_client_workflow.py`.
- [x] T011 [P] Integration test for Realtor workflow in `backend/tests/integration/test_realtor_workflow.py`.
- [x] T012 [P] Integration test for Affiliate workflow in `backend/tests/integration/test_affiliate_workflow.py`.
- [x] T013 [P] Integration test for Admin workflow in `backend/tests/integration/test_admin_workflow.py`.

## Phase 3.3: Core Implementation (ONLY after tests are failing)
### Backend
- [x] T014 [P] Create User model in `backend/src/models/user.py`.
- [x] T015 [P] Create Property model in `backend/src/models/property.py`.
- [x] T016 [P] Create Lead model in `backend/src/models/lead.py`.
- [x] T017 [P] Create Enquiry model in `backend/src/models/enquiry.py`.
- [x] T018 [P] Create AffiliateLink model in `backend/src/models/affiliate.py`.
- [x] T019 [P] Create Commission model in `backend/src/models/commission.py`.
- [x] T020 [P] Create Payout model in `backend/src/models/payout.py`.
- [x] T021 Implement `GET /users` endpoint in `backend/src/api/users.py`.
- [x] T022 Implement `POST /users` endpoint in `backend/src/api/users.py`.
- [x] T023 Implement `GET /properties` endpoint in `backend/src/api/properties.py`.
- [x] T024 Implement `POST /properties` endpoint in `backend/src/api/properties.py`.
- [x] T025 Implement `POST /enquiries` endpoint in `backend/src/api/enquiries.py`.

### Frontend
- [x] T026 [P] Implement shared Navbar component in `components/nav.py` by reusing the existing `nav.py` component from the `components/` folder and adapting it to the design system defined in the `docs/` folder.
- [x] T027 [P] Implement shared Sidebar component in `components/sidebar.py` by reusing existing components and adhering to the design system from the `docs/` folder.
- [x] T028 [P] Implement shared Card component in `components/card.py` by reusing the existing `card.py` component and the design system from the `docs/` folder.
- [x] T029 [P] Implement shared Table component in `components/table.py` by reusing the existing `product_table.py` component and the design system from the `docs/` folder.
- [x] T030 [P] Implement shared Modal component in `components/modal.py` by reusing existing components and the design system from the `docs/` folder.
- [x] T031 Implement Admin dashboard page in `pages/admin.py` using the shared components and the design system defined in the `docs/` folder.
- [x] T032 Implement Realtor dashboard page in `pages/realtor.py` using the shared components and the design system defined in the `docs/` folder.
- [x] T033 Implement Affiliate dashboard page in `pages/affiliate.py` using the shared components and the design system defined in the `docs/` folder.
- [x] T034 Implement Client dashboard page in `pages/client.py` using the shared components and the design system defined in the `docs/` folder.

## Phase 3.4: Integration
- [x] T035 Connect User service to the database.
- [x] T036 Connect Property service to the database.
- [x] T037 Implement authentication and authorization middleware.

## Phase 3.5: Polish
- [ ] T038 [P] Add unit tests for input validation.
- [ ] T039 [P] Write documentation for the API.

## Dependencies
- T002-T004 depend on T001.
- T005-T013 depend on T002-T004.
- T014-T034 depend on T005-T013 (tests failing).
- T035-T037 depend on T014-T034.
- T038-T039 can be done after T037.

## Parallel Example
```
# Launch T005-T009 together:
Task: "Contract test for GET /users in backend/tests/contract/test_users.py"
Task: "Contract test for POST /users in backend/tests/contract/test_users.py"
Task: "Contract test for GET /properties in backend/tests/contract/test_properties.py"
Task: "Contract test for POST /properties in backend/tests/contract/test_properties.py"
Task: "Contract test for POST /enquiries in backend/tests/contract/test_enquiries.py"
```
