# Auth Verification Skill

## Description
Handles JWT token verification and user authentication across the application.

## Capabilities
- Decode and verify JWT tokens
- Extract user ID from tokens
- Validate token expiration
- Verify token signature
- Attach user context to requests
- Handle authentication errors

## Implementation Notes
- Use BETTER_AUTH_SECRET for token verification
- Verify user ID matches in token and request
- Handle expired tokens appropriately
- Implement middleware for automatic verification
- Secure token storage and transmission