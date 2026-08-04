Backend Architecture

1. Vision
2. Design Principles
3. Project Structure
4. Layer Responsibilities
5. Dependency Rules
6. Service Architecture
7. Repository Architecture
8. Transaction Strategy
9. API Design Standards
10. Validation Strategy
11. Error Handling
12. Authentication & Authorization
13. Logging & Audit
14. Testing Strategy
15. Coding Standards
16. Future Module Architecture


# BusinessOS Backend Architecture

## Vision

BusinessOS is a production-grade, modular, AI-first SaaS platform designed using Clean Architecture principles.

The architecture is designed to:

- Scale across multiple business modules.
- Maintain clear separation of concerns.
- Keep business logic independent from frameworks.
- Enable independent testing of each layer.
- Support long-term maintainability.

Every new module added to the platform must follow this architecture without exception.

---

## Core Design Principles

1. Single Responsibility Principle
   - Every class has one responsibility.

2. Separation of Concerns
   - API handles HTTP.
   - Services handle business logic.
   - Repositories handle persistence.
   - Models represent database entities.

3. Feature-Oriented Organization
   - Services are grouped by business capability.
   - Each file represents one business use case.

4. Dependency Direction

Client
→ API
→ Service
→ Repository
→ Database

Dependencies must never flow in the opposite direction.

5. Consistency Over Cleverness

Every module must follow the same architecture, naming conventions, and coding standards.


---

# Project Structure

The backend follows a layered, feature-oriented architecture.

```
apps/api/app/
│
├── api/                    # FastAPI routers
│   └── v1/
│
├── core/                   # Application configuration
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
│
├── db/
│   ├── base.py
│   ├── session.py
│   └── models/
│
├── schemas/                # Request & Response DTOs
│
├── repositories/           # Database access layer
│
├── services/               # Business use cases
│   ├── organisation/
│   ├── membership/
│   ├── invitation/
│   ├── billing/
│   ├── workflow/
│   ├── ai/
│   └── common/
│
├── workers/                # Background jobs
│
├── integrations/           # External services
│
├── utils/                  # Shared utilities
│
└── main.py
```

---

## Layer Responsibilities

| Layer | Responsibility |
|--------|----------------|
| API | HTTP endpoints |
| Schemas | Request & Response validation |
| Services | Business use cases |
| Repositories | Database operations |
| Models | Database entities |
| Database | Persistent storage |

Each layer has exactly one responsibility.

Business logic must never appear in the API layer.

SQL must never appear in the Service layer.

HTTP concepts must never appear in the Repository layer.


---

# Dependency Rules

## Dependency Flow

All dependencies must flow in one direction only.

```
Client
    │
    ▼
API Layer
    │
    ▼
Schema Validation
    │
    ▼
Service Layer
    │
    ▼
Repository Layer
    │
    ▼
Database Models
    │
    ▼
Database
```

Dependencies must never flow in the opposite direction.

---

## API Layer

The API layer is responsible only for HTTP communication.

### Responsibilities

- Receive HTTP requests.
- Validate request schemas.
- Authenticate users.
- Call the appropriate Service.
- Return HTTP responses.

### Forbidden

- Business logic
- SQL queries
- Database transactions
- Complex validation
- Repository orchestration

---

## Service Layer

The Service layer implements business use cases.

### Responsibilities

- Business rules
- Validation
- Repository orchestration
- Authorization checks
- Transaction management
- Domain workflows

### Allowed Dependencies

- Repositories
- Schemas
- Models
- Common utilities

### Forbidden

- HTTP request handling
- FastAPI responses
- SQLAlchemy queries
- Direct database sessions inside business logic

---

## Repository Layer

Repositories provide access to persistent storage.

### Responsibilities

- Read data
- Insert data
- Update data
- Delete data

Repositories abstract database operations from business logic.

### Forbidden

- Business rules
- Authentication
- Authorization
- HTTP concepts
- External API calls

---

## Database Models

Models represent database tables.

Models should contain:

- Table definitions
- Relationships
- Constraints
- Indexes

Models should not contain business workflows.

---

## General Rules

✓ API can call Services.

✓ Services can call Repositories.

✓ Repositories can use Models.

✓ Models never call Services.

✓ Repositories never call APIs.

✓ APIs never access the database directly.

Violation of these rules requires architectural review.


---

# Repository Standards

Repositories are responsible only for persistence.

A repository is the single entry point to the database for a specific aggregate.

---

## Responsibilities

Repositories may:

- Query records
- Insert records
- Update records
- Delete records
- Build SQLAlchemy queries
- Handle eager/lazy loading

Repositories must never contain business logic.

---

## Naming Convention

Repository names follow:

```

<Entity>Repository

```

Examples

```

UserRepository

OrganisationRepository

InvitationRepository

RoleRepository

PermissionRepository

```

---

## File Structure

```

repositories/
│
├── user_repository.py
├── organisation_repository.py
├── invitation_repository.py
├── organisation_member_repository.py
├── role_repository.py
└── permission_repository.py

```

---

## Standard Repository Interface

Every repository should expose only persistence methods.

Typical methods include:

```

get_by_id()

get_all()

create()

update()

delete()

exists()

```

Additional methods should exist only when required by business needs.

Example:

```

get_by_email()

get_by_slug()

get_by_token()

get_by_username()

```

---

## Forbidden Responsibilities

Repositories must never:

- Validate business rules
- Send emails
- Publish events
- Call external APIs
- Perform authentication
- Perform authorization
- Parse HTTP requests
- Return HTTP responses

---

## Transaction Strategy

Repositories participate in transactions.

Repositories should not decide business workflows.

The Service layer coordinates multiple repositories.

Long-term architecture:

```

Service
│
├── Repository A
├── Repository B
├── Repository C
│
└── Commit / Rollback

```

Repositories should be transaction-aware but not workflow-aware.

---

## Error Handling

Repositories should raise only persistence-related exceptions.

Business exceptions belong in the Service layer.

---

## Performance Guidelines

Repositories should:

- Use indexed queries whenever possible.
- Avoid N+1 query problems.
- Use eager loading where appropriate.
- Return only required data.
- Keep queries efficient.

---

## Repository Design Rules

✓ One repository per aggregate.

✓ Keep methods small.

✓ One responsibility per method.

✓ No duplicated queries.

✓ No business decisions.

✓ Repository methods should be deterministic.

---

## Example Dependency

```

CreateOrganisationService
│
├── OrganisationRepository
├── RoleRepository
├── UserRepository
└── OrganisationMemberRepository

```

Repositories never depend on Services.

Services depend on Repositories.



---

# Service Standards

The Service layer is the heart of the BusinessOS backend.

Every business workflow must be implemented as an independent use case.

Services orchestrate repositories and implement business rules.

---

# Philosophy

Services answer one business question.

Examples:

- How is an organisation created?
- How is a member invited?
- How is a subscription upgraded?
- How is an AI agent executed?

Every service should have exactly one responsibility.

---

# Feature Organization

Services are organized by business capability.

```
services/
│
├── organisation/
│   ├── create_organisation.py
│   ├── update_organisation.py
│   ├── delete_organisation.py
│   ├── get_organisation.py
│   ├── list_organisations.py
│   └── __init__.py
│
├── membership/
│   ├── add_member.py
│   ├── remove_member.py
│   ├── change_role.py
│   └── __init__.py
│
├── invitation/
│   ├── invite_member.py
│   ├── accept_invitation.py
│   ├── revoke_invitation.py
│   └── __init__.py
│
└── common/
```

Each file represents exactly one business use case.

---

# Naming Convention

Files

```
create_organisation.py
invite_member.py
accept_invitation.py
```

Classes

```
CreateOrganisationService
InviteMemberService
AcceptInvitationService
```

---

# Public Interface

Every Service exposes exactly one public method.

```python
async def execute(...)
```

No additional public methods.

Helper methods must remain private.

Example

```python
class CreateOrganisationService:

    async def execute(...):
        ...

    async def _validate_slug(...):
        ...

    async def _load_owner(...):
        ...

    async def _create_organisation(...):
        ...

    async def _assign_owner(...):
        ...
```

---

# Responsibilities

Services are responsible for:

- Business rules
- Validation
- Authorization
- Repository orchestration
- Transactions
- Workflow coordination
- Event publishing
- Audit logging

---

# Forbidden Responsibilities

Services must never:

- Execute SQL
- Define database tables
- Parse HTTP requests
- Return HTTP responses
- Contain FastAPI routers

---

# Dependency Rules

A Service may depend on:

- Repositories
- Schemas
- Domain Models
- Shared Utilities
- Other Services (only when explicitly approved)

Services must never depend on:

- API Routers
- Controllers
- HTTP Request objects
- Database Sessions directly

---

# Validation Strategy

Validation occurs in three stages.

Stage 1

Schema Validation

Examples:

- Required fields
- Email format
- String length

Handled by Pydantic.

---

Stage 2

Business Validation

Examples:

- Slug already exists
- User already belongs to organisation
- Subscription expired

Handled by Services.

---

Stage 3

Database Constraints

Examples:

- Unique indexes
- Foreign keys

Handled by PostgreSQL.

---

# Error Handling

Business failures should raise domain-specific exceptions.

Examples

```
OrganisationAlreadyExists

InvitationExpired

PermissionDenied

MemberAlreadyExists
```

Avoid generic ValueError for business rules.

---

# Transaction Ownership

One business workflow equals one transaction.

Example

```
CreateOrganisation

↓

Create Organisation

↓

Assign Owner

↓

Create Membership

↓

Audit Log

↓

Commit
```

If any step fails:

```
Rollback Transaction
```

---

# Service Checklist

Every Service must satisfy:

✓ One business responsibility

✓ One public execute() method

✓ Small private helper methods

✓ Repository orchestration only

✓ No SQL

✓ No HTTP

✓ Easy to unit test

✓ Deterministic behaviour

---

# Example

```
POST /organisations

↓

Organisation Router

↓

CreateOrganisationService.execute()

↓

OrganisationRepository

↓

OrganisationMemberRepository

↓

RoleRepository

↓

Commit

↓

Response
```

The Service layer is the only place where multiple repositories are coordinated.



CTO Decision (New Standard)

From this point forward, every new feature must start by answering these four questions before any code is written:

Which feature module does this belong to?
Organisation, Membership, Billing, AI, Workflow, etc.
What is the single business use case?
Create, Invite, Approve, Cancel, Execute, Publish.
Which repositories are involved?
What transaction boundary does this workflow require?

If a feature cannot answer these four questions clearly, it is not ready to implement.


---

# API Standards

The API layer is responsible only for HTTP communication.

It is the entry point into the application and delegates all business operations to the Service layer.

---

# API Responsibilities

The API layer may:

- Receive HTTP requests
- Validate request schemas
- Authenticate users
- Authorize access (basic route-level checks)
- Call Services
- Return HTTP responses
- Map exceptions to HTTP status codes

---

# Forbidden Responsibilities

The API layer must never:

- Execute business logic
- Execute SQL queries
- Access repositories directly
- Coordinate multiple repositories
- Implement workflows
- Perform complex validation

---

# Standard Request Flow

```
Client

↓

FastAPI Router

↓

Pydantic Validation

↓

Authentication

↓

Service.execute()

↓

Repository

↓

Database

↓

Response Schema

↓

Client
```

Every endpoint follows exactly the same lifecycle.

---

# Router Organization

```
api/
└── v1/
    ├── auth.py
    ├── organisations.py
    ├── memberships.py
    ├── invitations.py
    ├── workspaces.py
    ├── projects.py
    ├── tasks.py
    └── ai.py
```

One router per business capability.

---

# Endpoint Naming

Use RESTful naming conventions.

## Organisations

```
POST   /organisations
GET    /organisations
GET    /organisations/{id}
PATCH  /organisations/{id}
DELETE /organisations/{id}
```

---

## Members

```
GET    /organisations/{id}/members

POST   /organisations/{id}/members

PATCH  /organisations/{id}/members/{member_id}

DELETE /organisations/{id}/members/{member_id}
```

---

## Invitations

```
POST   /invitations

GET    /invitations/{token}

POST   /invitations/{token}/accept

DELETE /invitations/{id}
```

---

# Router Pattern

Every endpoint should be minimal.

Example

```python
@router.post(
    "",
    response_model=OrganisationResponse,
)
async def create_organisation(
    payload: OrganisationCreate,
    current_user: User = Depends(get_current_user),
):

    return await create_organisation_service.execute(
        name=payload.name,
        slug=payload.slug,
        description=payload.description,
        owner_id=current_user.id,
    )
```

Notice:

- No SQL
- No Repository
- No Business Rules

---

# Dependency Injection

Dependencies should be injected through FastAPI.

Examples

- Database Session
- Current User
- Permissions
- Service Factory

Avoid constructing repositories inside routers.

---

# Response Models

Every endpoint must return a Schema.

Never return SQLAlchemy models directly.

Example

```
OrganisationResponse

InvitationResponse

UserResponse

MemberResponse
```

---

# HTTP Status Codes

Follow REST standards.

```
200 OK

201 Created

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error
```

---

# Error Mapping

Business Exceptions

↓

HTTP Exceptions

Example

```
OrganisationAlreadyExists

↓

409 Conflict
```

```
InvitationExpired

↓

410 Gone
```

```
PermissionDenied

↓

403 Forbidden
```

---

# Versioning

Every public endpoint belongs to a version.

Example

```
/api/v1/...
```

Future breaking changes create

```
/api/v2/...
```

---

# API Checklist

Every endpoint must satisfy:

✓ Uses request schema

✓ Uses response schema

✓ Calls exactly one Service

✓ No SQL

✓ No Repository usage

✓ No business logic

✓ Uses dependency injection

✓ Proper HTTP status codes

✓ Fully documented

---

# Architecture Summary

```
Client

↓

FastAPI Router

↓

Schema Validation

↓

Authentication

↓

Service.execute()

↓

Repositories

↓

Database

↓

Response Schema

↓

Client
```

The API layer coordinates HTTP only.

All business decisions belong to the Service layer.


---

# Transaction Strategy

## Purpose

A transaction guarantees that a complete business workflow either:

- completes successfully, or
- rolls back completely.

There must never be a partially completed business operation.

---

# Principle

One business use case equals one transaction.

Examples

- Create Organisation
- Invite Member
- Accept Invitation
- Upgrade Subscription
- Create Workspace
- Execute Workflow

Each executes inside a single transaction.

---

# Transaction Ownership

The Service layer owns transactions.

```
API

↓

Service

↓

Repository

↓

Database
```

Repositories never decide when to commit.

Services decide when a business operation has successfully completed.

---

# Repository Rules

Repositories may:

- SELECT
- INSERT
- UPDATE
- DELETE

Repositories should not coordinate multiple business operations.

Repositories should not decide transaction boundaries.

---

# Service Rules

Services are responsible for:

- Begin transaction
- Coordinate repositories
- Commit transaction
- Rollback transaction
- Return business result

---

# Example Workflow

Create Organisation

```
Begin Transaction

↓

Validate Slug

↓

Load Owner

↓

Load Administrator Role

↓

Create Organisation

↓

Create Organisation Member

↓

Write Audit Log

↓

Commit
```

If any step fails

```
Rollback
```

No data should remain partially written.

---

# Future Repository Pattern

Current implementation

```python
repository.create()

↓

commit()
```

Future implementation

```python
repository.add(entity)
```

The Service performs

```python
await session.commit()
```

This enables one transaction across multiple repositories.

---

# Rollback Strategy

Any unexpected failure during a workflow results in

```
Rollback Transaction
```

Examples

- Database exception
- Constraint violation
- External service failure
- Validation failure after partial work

The database must return to its previous consistent state.

---

# Nested Operations

A Service may call multiple repositories.

Example

```
CreateOrganisationService

↓

OrganisationRepository

↓

RoleRepository

↓

OrganisationMemberRepository

↓

AuditRepository
```

Only one transaction wraps the entire workflow.

---

# Long Running Operations

Do not include external network operations inside a database transaction.

Examples

Avoid

```
Create Organisation

↓

Commit Pending

↓

Send Email

↓

Wait 5 seconds
```

Instead

```
Create Organisation

↓

Commit

↓

Publish Event

↓

Email Worker

↓

Send Email
```

Transactions should remain short.

---

# Future Event Architecture

Business workflow

↓

Commit

↓

Domain Event

↓

Background Worker

↓

Email

↓

Notifications

↓

Webhooks

Database consistency must never depend on external systems.

---

# Transaction Checklist

Every business workflow must satisfy

✓ One transaction

✓ One commit

✓ Rollback on failure

✓ No partial updates

✓ Repository coordination inside Service

✓ External APIs execute after commit

---

# Current PR-006 Strategy

Current repositories still call

```
commit()
```

This is acceptable temporarily to keep PR-006 focused.

After PR-006 is merged

Create

```
PR-007
Repository Transaction Refactor
```

Goals

- Remove commit() from repositories.
- Move transaction ownership into Services.
- Introduce Unit of Work if needed.
- Update all existing Services.

This establishes the long-term transaction architecture for the entire platform.


---

# Error Handling Strategy

## Purpose

Errors must be:

- Predictable
- Consistent
- Traceable
- Meaningful

The same error should always produce the same HTTP response.

---

# Error Flow

```
Client

↓

FastAPI Router

↓

Service

↓

Repository

↓

Database
```

If an error occurs

```
Repository Exception

↓

Service Exception

↓

API Exception Handler

↓

HTTP Response

↓

Client
```

---

# Error Categories

BusinessOS classifies errors into five categories.

## 1. Validation Errors

Raised when user input is invalid.

Examples

- Invalid email
- Invalid slug
- Missing required field

HTTP Status

```
422 Unprocessable Entity
```

Handled by

```
Pydantic
```

---

## 2. Business Errors

Raised when business rules fail.

Examples

```
OrganisationAlreadyExists

MemberAlreadyExists

InvitationExpired

WorkspaceLimitExceeded

SubscriptionInactive
```

HTTP Status

```
400

403

404

409

410
```

depending on the business rule.

---

## 3. Authorization Errors

Raised when a user lacks permission.

Examples

```
PermissionDenied

OrganisationAccessDenied

RoleNotAllowed
```

HTTP Status

```
403 Forbidden
```

---

## 4. Infrastructure Errors

Raised by external systems.

Examples

```
Database unavailable

Redis unavailable

Email provider unavailable

Object storage unavailable
```

HTTP Status

```
500 Internal Server Error

503 Service Unavailable
```

---

## 5. Unexpected Errors

Programming errors.

Examples

```
AttributeError

TypeError

RuntimeError
```

These must be logged.

Users should receive a generic response.

```
500 Internal Server Error
```

---

# Exception Hierarchy

Create a common exception hierarchy.

```
BusinessOSError
│
├── ValidationError
│
├── BusinessRuleError
│   ├── OrganisationAlreadyExists
│   ├── MemberAlreadyExists
│   ├── InvitationExpired
│   └── SubscriptionExpired
│
├── AuthorizationError
│   ├── PermissionDenied
│   └── AccessDenied
│
├── InfrastructureError
│
└── ExternalServiceError
```

Every custom exception inherits from a common base.

---

# Repository Errors

Repositories should never raise business exceptions.

Repositories may raise

- Database exceptions
- SQLAlchemy exceptions

The Service layer converts persistence failures into business exceptions where appropriate.

---

# Service Errors

Services are responsible for business exceptions.

Example

```
Slug already exists

↓

Raise OrganisationAlreadyExists
```

Never raise

```
ValueError
```

for business rules.

---

# API Layer

The API layer should never contain business logic.

Its responsibility is only to map exceptions.

Example

```
OrganisationAlreadyExists

↓

409 Conflict
```

```
PermissionDenied

↓

403 Forbidden
```

```
InvitationExpired

↓

410 Gone
```

---

# Logging

Unexpected exceptions must be logged with:

- Timestamp
- User ID
- Organisation ID
- Request ID
- Stack trace

Business exceptions should be logged at INFO or WARNING level.

Infrastructure failures should be logged at ERROR level.

Unexpected failures should be logged at CRITICAL level.

---

# Client Response

Never expose internal implementation details.

Bad

```json
{
    "detail": "IntegrityError: duplicate key value violates constraint..."
}
```

Good

```json
{
    "error": "OrganisationAlreadyExists",
    "message": "An organisation with this slug already exists."
}
```

---

# Error Checklist

Every exception should satisfy

✓ Human-readable

✓ Machine-readable

✓ Logged

✓ Consistent HTTP status

✓ No internal implementation leakage

✓ Traceable through logs

✓ Actionable for developers




---

# Testing Strategy

## Vision

Every business feature must be testable independently.

Testing is organized by architectural layer.

```
Unit Tests

↓

Repository Tests

↓

Service Tests

↓

API Tests

↓

Integration Tests

↓

End-to-End Tests
```

No feature is considered complete until the appropriate tests exist.

---

# Testing Pyramid

```
               E2E
             /     \
        Integration
         /         \
      API Tests
     /             \
  Service Tests
 /                 \
Repository Tests
       |
   Unit Tests
```

Most tests should exist at the Service layer.

---

# Test Structure

```
tests/
│
├── unit/
│
├── repositories/
│
├── services/
│
├── api/
│
├── integration/
│
├── fixtures/
│
└── conftest.py
```

---

# Unit Tests

Purpose

Test individual functions.

Examples

- Utility functions
- Validators
- Slug generation
- Permission helpers

Unit tests should not access the database.

---

# Repository Tests

Purpose

Verify database operations.

Examples

- Create Organisation
- Find User
- Delete Invitation
- Update Member

Repository tests verify:

- Queries
- Relationships
- Constraints
- Indexes

---

# Service Tests

Highest priority.

Services contain business logic.

Examples

```
CreateOrganisationService

InviteMemberService

AcceptInvitationService

UpgradeSubscriptionService
```

Typical scenarios

✓ Happy path

✓ Validation failure

✓ Authorization failure

✓ Duplicate data

✓ Missing records

✓ Transaction rollback

Every business rule should have a corresponding Service test.

---

# API Tests

Verify HTTP behavior.

Examples

```
POST /organisations

GET /organisations

PATCH /organisations/{id}
```

Verify

- Status code
- Response schema
- Authentication
- Authorization
- Error responses

API tests do not verify business rules in detail.

---

# Integration Tests

Verify multiple components working together.

Examples

```
API

↓

Service

↓

Repository

↓

Database
```

Integration tests ensure the complete workflow behaves correctly.

---

# End-to-End Tests

Verify complete user journeys.

Examples

```
Register

↓

Login

↓

Create Organisation

↓

Invite Member

↓

Accept Invitation
```

E2E tests simulate real user behavior.

---

# Mocking Strategy

Mock only external dependencies.

Examples

- Email provider
- Payment gateway
- AI provider
- Redis
- Object storage

Do not mock repositories during repository tests.

Do not mock services during service tests.

---

# Test Data

Use factories or fixtures.

Avoid manually creating repetitive test data.

Example

```
tests/
└── fixtures/
    ├── users.py
    ├── organisations.py
    ├── roles.py
    └── invitations.py
```

---

# Coverage Goals

Minimum targets

```
Repositories

90%

Services

95%

API

85%

Overall

90%
```

Coverage percentage is not the primary goal.

Meaningful tests are more important than coverage numbers.

---

# Naming Convention

```
test_create_organisation_success()

test_create_organisation_duplicate_slug()

test_invite_member_success()

test_invite_member_permission_denied()
```

Names should describe the scenario.

---

# Testing Checklist

Every feature should include

✓ Happy path

✓ Invalid input

✓ Unauthorized access

✓ Forbidden access

✓ Missing resource

✓ Duplicate resource

✓ Database failure

✓ Transaction rollback

✓ Correct response model

✓ Correct status code

---

# PR Requirement

A Pull Request is not complete until

✓ Code compiles

✓ Tests pass

✓ Coverage maintained

✓ No failing integration tests

✓ No failing API tests

Testing is part of development, not a separate activity.



---

# Coding Standards

## Purpose

BusinessOS follows a single coding standard across the entire backend.

Consistency is more valuable than individual coding style.

---

# General Principles

Code should be

- Simple
- Readable
- Predictable
- Testable
- Maintainable

Every engineer should be able to understand a file without knowing who wrote it.

---

# File Naming

Use snake_case.

Examples

```
create_organisation.py
invite_member.py
organisation_repository.py
permission_service.py
```

Never use

```
CreateOrganisation.py

CreateOrganisationService.py
```

---

# Class Naming

Use PascalCase.

Examples

```
CreateOrganisationService

OrganisationRepository

InvitationResponse

PermissionDenied
```

---

# Function Naming

Use snake_case.

Examples

```python
create_user()

get_by_slug()

assign_role()

accept_invitation()
```

---

# Variables

Names should describe intent.

Good

```python
organisation

current_user

admin_role

existing_member
```

Bad

```python
obj

temp

data

value

x
```

---

# Method Size

Target

```
10–30 lines
```

Maximum

```
50 lines
```

If longer, extract helper methods.

---

# Function Responsibility

Every function should perform one task.

Good

```
_validate_slug()

_load_owner()

_assign_owner()
```

Bad

```
create_everything()
```

---

# Comments

Write comments only when explaining intent.

Good

```python
# Prevent duplicate organisation slugs
```

Bad

```python
# Increment i
i += 1
```

Code should explain how.

Comments explain why.

---

# Docstrings

Every public class and public method should have a docstring.

Example

```python
class CreateOrganisationService:
    """Creates a new organisation and assigns its owner."""
```

---

# Imports

Standard Library

↓

Third-party

↓

Application

Example

```python
from uuid import UUID

from sqlalchemy import select

from app.db.models.organisation import Organisation
```

Separate groups with one blank line.

---

# Dependency Injection

Inject dependencies.

Never instantiate repositories inside services.

Good

```python
def __init__(
    self,
    organisation_repository,
):
```

Bad

```python
repository = OrganisationRepository(db)
```

---

# Business Logic

Business logic belongs only inside Services.

Never place business logic in

- Routers
- Repositories
- Models

---

# Magic Values

Avoid hardcoded values.

Bad

```python
role = "Administrator"
```

Prefer

```python
SYSTEM_ADMIN_ROLE = "Administrator"
```

or configuration/constants when appropriate.

---

# Logging

Use structured logging.

Every log should include context.

Examples

- User ID
- Organisation ID
- Request ID
- Action

Never log passwords, tokens, or secrets.

---

# Type Hints

All public methods require type hints.

Example

```python
async def execute(
    self,
    *,
    owner_id: UUID,
) -> Organisation:
```

---

# Formatting

Project standards

- Ruff
- Black
- isort

Formatting is automatic.

Developers should not manually format code.

---

# Complexity

Avoid deep nesting.

Bad

```
if
    if
        if
            if
```

Prefer early returns.

---

# Constants

Shared constants belong in

```
app/core/constants.py
```

Avoid duplicated strings throughout the project.

---

# Definition of Done

A file is complete when

✓ Compiles

✓ Typed

✓ Linted

✓ Formatted

✓ Tested

✓ Documented

✓ Reviewed

---

# Engineering Principles

BusinessOS follows these principles.

- SOLID
- DRY
- KISS
- YAGNI
- Clean Architecture
- Explicit over implicit
- Readability over cleverness
- Consistency over personal preference

Every contribution to the codebase should reinforce these principles.


---

# Module Blueprint

## Purpose

Every BusinessOS module follows the same architecture.

Regardless of whether the feature is:

- Organisation
- Workspace
- Project
- Task
- Workflow
- Billing
- AI
- Notification

…the implementation structure remains identical.

Consistency enables maintainability and predictable development.

---

# Standard Module Structure

```
module/
│
├── api/
│
├── schemas/
│
├── services/
│
├── repositories/
│
├── models/
│
├── tests/
│
└── __init__.py
```

Every module owns its complete business functionality.

---

# Service Blueprint

Every business use case is implemented as a dedicated Service.

Examples

```
CreateOrganisationService

UpdateOrganisationService

DeleteOrganisationService

InviteMemberService

AcceptInvitationService
```

Every Service exposes exactly one public method.

```
execute()
```

---

# Repository Blueprint

Every aggregate has one Repository.

Example

```
OrganisationRepository

UserRepository

InvitationRepository

WorkspaceRepository
```

Responsibilities

- Query
- Insert
- Update
- Delete

Nothing else.

---

# Schema Blueprint

Every module contains

### Request Schemas

```
OrganisationCreate

OrganisationUpdate

InvitationCreate
```

### Response Schemas

```
OrganisationResponse

InvitationResponse

MemberResponse
```

Never expose ORM models directly.

---

# API Blueprint

Every module exposes REST endpoints.

Example

```
POST

GET

PATCH

DELETE
```

Router responsibilities

- Receive request
- Validate
- Authenticate
- Call Service
- Return response

Nothing more.

---

# Testing Blueprint

Every module includes

```
tests/
│
├── repository/
├── service/
├── api/
└── integration/
```

Every business workflow has at least one Service test.

---

# Typical Request Flow

```
Client

↓

FastAPI Router

↓

Pydantic Schema

↓

Authentication

↓

Service.execute()

↓

Repositories

↓

Database

↓

Response Schema

↓

Client
```

Every module follows this flow.

---

# Pull Request Blueprint

Every feature PR follows the same lifecycle.

```
Requirement

↓

Design

↓

Model

↓

Migration

↓

Schema

↓

Repository

↓

Service

↓

API

↓

Tests

↓

Documentation

↓

Review

↓

Merge
```

No stage is skipped.

---

# Definition of Done

A module is complete only when:

✓ Database models implemented

✓ Alembic migration created

✓ Schemas implemented

✓ Repository implemented

✓ Service implemented

✓ API endpoints implemented

✓ Authentication integrated

✓ Authorization verified

✓ Unit tests written

✓ Service tests written

✓ API tests written

✓ Integration tests written

✓ Documentation updated

✓ Ruff passes

✓ Formatting passes

✓ Type checking passes

✓ All tests pass

✓ Code reviewed

✓ Merged into main

---

# Pull Request Checklist

Before opening a PR

- [ ] Architecture follows the handbook
- [ ] Folder structure correct
- [ ] Naming conventions followed
- [ ] Business logic only in Services
- [ ] Repository contains no business logic
- [ ] API contains no business logic
- [ ] Tests added
- [ ] Documentation updated
- [ ] Ruff passes
- [ ] Mypy passes
- [ ] Pytest passes

---

# Future Modules

Every future module will follow this exact template.

Examples

```
Workspace Module

Project Module

Task Module

Workflow Module

Knowledge Base Module

Notification Module

Billing Module

Subscription Module

Audit Module

AI Module

Analytics Module
```

No module should introduce a different architecture.

---

# Architecture Governance

The backend architecture is a project standard.

Changes to:

- Layer responsibilities
- Dependency direction
- Transaction strategy
- Folder structure
- Naming conventions

must be reviewed before implementation.

Architectural consistency has higher priority than individual implementation preferences.

---

# Architecture Version

Version: 1.0

Status: Approved

This document is the engineering standard for all BusinessOS backend development.