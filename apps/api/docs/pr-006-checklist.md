# PR-006: User & Organisation Management Checklist

## Models
- [x] Organisation
- [x] OrganisationMember
- [x] Invitation

## Database
- [x] Alembic Migration
- [x] Foreign Keys
- [x] Relationships

## Schemas
- [x] Organisation
- [x] OrganisationMember
- [x] Invitation

## Repositories
- [x] OrganisationRepository
- [x] OrganisationMemberRepository
- [x] InvitationRepository

## Services

### Organisation
- [ ] CreateOrganisationService
- [ ] UpdateOrganisationService
- [ ] DeleteOrganisationService
- [ ] GetOrganisationService
- [ ] ListOrganisationsService

### Membership
- [ ] AddMemberService
- [ ] RemoveMemberService
- [ ] ChangeMemberRoleService
- [ ] ListMembersService

### Invitation
- [ ] InviteMemberService
- [ ] AcceptInvitationService
- [ ] RevokeInvitationService
- [ ] GetInvitationService

## API

### Organisations
- [ ] POST /organisations
- [ ] GET /organisations
- [ ] GET /organisations/{id}
- [ ] PATCH /organisations/{id}
- [ ] DELETE /organisations/{id}

### Members
- [ ] GET /organisations/{id}/members
- [ ] POST /organisations/{id}/members
- [ ] PATCH /organisations/{id}/members/{member_id}
- [ ] DELETE /organisations/{id}/members/{member_id}

### Invitations
- [ ] POST /invitations
- [ ] GET /invitations/{token}
- [ ] POST /invitations/{token}/accept
- [ ] DELETE /invitations/{id}

## Testing
- [ ] Repository Tests
- [ ] Service Tests
- [ ] API Tests
- [ ] Integration Tests

## Documentation
- [ ] OpenAPI Documentation
- [ ] Architecture Review
- [ ] Final PR Review
