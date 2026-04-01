---
name: memstack-development-api-designer
description: "Use this skill when the user says 'design API', 'API endpoints', 'REST API', 'API designer', 'route structure', 'API architecture', or is designing RESTful API routes, request/response schemas, and endpoint organization. Do NOT use for API security audits or database design."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🔌 API Designer — Designing routes, validation, and handler patterns...
*Produces production-ready Next.js App Router API routes with auth guards, Zod validation, typed responses, and consistent error handling.*

## Activation

When this skill activates, output:

`🔌 API Designer — Designing API routes and handlers...`

Then execute the protocol below.

| Context | Status |
|---------|--------|
| User says "design API" or "create API route" or "add endpoint" | ACTIVE |
| User says "REST API" or "route handler" | ACTIVE |
| Building a new feature that needs API routes | ACTIVE |
| Designing webhook endpoints | ACTIVE |
| Discussing API concepts or REST theory | DORMANT |
| Working on frontend components (not API layer) | DORMANT |

### Anti-patterns

| Trap | Reality Check |
|------|---------------|
| "Auth is handled by middleware" | Middleware can be bypassed. Every route handler must verify auth independently. |
| "I'll validate input later" | Unvalidated input is the root of injection, type errors, and 500s. Zod first, logic second. |
| "Return 200 for everything" | Status codes are the API contract. 401 vs 403 vs 404 vs 422 mean different things to clients. |
| "Error details help debugging" | Stack traces and internal errors help attackers. Return safe messages, log details server-side. |
| "Rate limiting is a nice-to-have" | Public endpoints without rate limits get abused within hours of deployment. |
| "TypeScript types are documentation enough" | Types exist at build time. Zod schemas validate at runtime. You need both. |

## Protocol

### Step 1: Design Route Structure

Map features to Next.js App Router file paths:

```
app/
  api/
    auth/
      login/route.ts          POST   - authenticate user
      logout/route.ts         POST   - clear session
      callback/route.ts       GET    - OAuth callback
    organizations/
      route.ts                GET    - list user's orgs
                              POST   - create org
      [orgId]/
        route.ts              GET    - get org details
                              PATCH  - update org
                              DELETE - delete org
        members/
          route.ts            GET    - list members
                              POST   - invite member
          [memberId]/
            route.ts          PATCH  - update role
                              DELETE - remove member
        projects/
          route.ts            GET    - list projects
                              POST   - create project
    webhooks/
      stripe/route.ts         POST   - Stripe webhook
      github/route.ts         POST   - GitHub webhook
```

**Naming conventions:**

| Convention | Rule | Example |
|------------|------|---------|
| Resource names | Plural nouns | `/organizations`, `/projects` |
| Dynamic segments | `[paramName]` camelCase | `[orgId]`, `[memberId]` |
| Nested resources | Parent/child path | `/organizations/[orgId]/projects` |
| Actions (non-CRUD) | Verb sub-path | `/auth/login`, `/reports/generate` |
| Webhooks | `/webhooks/{provider}` | `/webhooks/stripe` |

**Output route table:**

```
Method  Path                              Auth    Description
GET     /api/organizations                 ✅     List user's organizations
POST    /api/organizations                 ✅     Create organization
GET     /api/organizations/[orgId]         ✅+org  Get organization details
PATCH   /api/organizations/[orgId]         ✅+org  Update organization
...
POST    /api/webhooks/stripe               🔑sig  Handle Stripe webhook
```

### Step 2: Auth Guard Pattern

Every protected route starts with the same two-step auth chain:

```typescript
import { getAuthContext } from '@/lib/auth';
import { verifyOrgAccess } from '@/lib/auth';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  req: NextRequest,
  { params }: { params: { orgId: string } }
) {
  // Step 1: Authenticate — who is this user?
  const auth = await getAuthContext(req);
  if (!auth) {
    return NextResponse.json(
      { error: 'Authentication required' },
      { status: 401 }
    );
  }

  // Step 2: Authorize — can they access this org?
  const access = await verifyOrgAccess(auth.userId, params.orgId);
  if (!access) {
    return NextResponse.json(
      { error: 'Access denied' },
      { status: 403 }
    );
  }

  // Now proceed with business logic...
}
```

**Auth decision matrix:**

| Route Type | Auth Required | Org Check | Example |
|-----------|--------------|-----------|---------|
| Public | ❌ | ❌ | `GET /api/health` |
| Authenticated | ✅ | ❌ | `GET /api/user/profile` |
| Org-scoped | ✅ | ✅ | `GET /api/organizations/[orgId]/projects` |
| Admin-only | ✅ | ✅ + role check | `DELETE /api/organizations/[orgId]` |
| Webhook | 🔑 Signature | ❌ | `POST /api/webhooks/stripe` |

### Step 3: Input Validation with Zod

Every route that accepts input validates it before any logic runs:

```typescript
import { z } from 'zod';

// Define schema next to the route handler
const createProjectSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  status: z.enum(['draft', 'active', 'archived']).default('draft'),
  settings: z.object({
    isPublic: z.boolean().default(false),
    tags: z.array(z.string().max(50)).max(10).default([]),
  }).optional(),
});

type CreateProjectInput = z.infer<typeof createProjectSchema>;

export async function POST(req: NextRequest) {
  // ... auth checks ...

  // Validate input
  const body = await req.json();
  const parsed = createProjectSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: parsed.error.flatten() },
      { status: 422 }
    );
  }

  // parsed.data is fully typed as CreateProjectInput
  const project = await createProject(parsed.data);
  return NextResponse.json({ data: project }, { status: 201 });
}
```

**Zod patterns for common fields:**

```typescript
// Reusable schemas
const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

const sortSchema = z.object({
  sortBy: z.string().default('created_at'),
  sortOrder: z.enum(['asc', 'desc']).default('desc'),
});

const uuidParam = z.string().uuid('Invalid ID format');

// Query params validation (GET routes)
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const query = paginationSchema.merge(sortSchema).safeParse(
    Object.fromEntries(searchParams)
  );
  // ...
}
```

### Step 4: Consistent Response Format

All responses follow a strict structure:

```typescript
// Success responses — always wrap in { data }
return NextResponse.json({ data: result });
return NextResponse.json({ data: results, meta: { total, page, limit } });

// Error responses — always wrap in { error }
return NextResponse.json({ error: 'Not found' }, { status: 404 });
return NextResponse.json(
  { error: 'Validation failed', details: zodError.flatten() },
  { status: 422 }
);
```

**Type definitions for responses:**

```typescript
// types/api.ts
export type ApiResponse<T> = {
  data: T;
  meta?: {
    total: number;
    page: number;
    limit: number;
  };
};

export type ApiError = {
  error: string;
  details?: unknown;
};

// Helper function
export function apiSuccess<T>(data: T, status = 200): NextResponse {
  return NextResponse.json({ data }, { status });
}

export function apiError(error: string, status: number, details?: unknown): NextResponse {
  return NextResponse.json({ error, ...(details && { details }) }, { status });
}
```

### Step 5: HTTP Status Codes

Use the correct status code for each situation:

| Code | Meaning | When to Use |
|------|---------|------------|
| `200` | OK | Successful GET, PATCH, or general success |
| `201` | Created | Successful POST that creates a resource |
| `204` | No Content | Successful DELETE (no response body) |
| `400` | Bad Request | Malformed request (invalid JSON, wrong Content-Type) |
| `401` | Unauthorized | Not authenticated (no token, expired session) |
| `403` | Forbidden | Authenticated but not authorized (wrong org, wrong role) |
| `404` | Not Found | Resource doesn't exist (or user can't see it — use 404 to avoid leaking existence) |
| `409` | Conflict | Duplicate resource (unique constraint violation) |
| `422` | Unprocessable Entity | Valid JSON but failed validation (Zod errors) |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Unexpected server error (log details, return safe message) |

**Key distinction — 401 vs 403 vs 404:**
- `401`: "I don't know who you are" → redirect to login
- `403`: "I know who you are, but you can't do this" → show permission error
- `404`: "This doesn't exist (or you can't know it exists)" → use for privacy-preserving access denial

### Step 6: Rate Limiting

Protect public and sensitive endpoints:

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '60 s'), // 10 requests per minute
  analytics: true,
});

// In route handler
export async function POST(req: NextRequest) {
  const ip = req.headers.get('x-forwarded-for') ?? 'anonymous';
  const { success, limit, remaining, reset } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: 'Rate limit exceeded. Try again later.' },
      {
        status: 429,
        headers: {
          'X-RateLimit-Limit': limit.toString(),
          'X-RateLimit-Remaining': remaining.toString(),
          'X-RateLimit-Reset': reset.toString(),
        },
      }
    );
  }

  // Continue with handler...
}
```

**Rate limit tiers:**

| Endpoint Type | Limit | Window |
|--------------|-------|--------|
| Auth (login, register) | 5 requests | 15 minutes |
| Public API | 60 requests | 1 minute |
| Authenticated API | 120 requests | 1 minute |
| Webhooks | 1000 requests | 1 minute |
| File upload | 10 requests | 1 hour |

### Step 7: Webhook Endpoints

Webhooks require signature verification instead of JWT auth:

```typescript
import { headers } from 'next/headers';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: NextRequest) {
  const body = await req.text(); // Raw body for signature verification
  const signature = req.headers.get('stripe-signature');

  if (!signature) {
    return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
  }

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  // Process event by type
  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutComplete(event.data.object);
      break;
    case 'customer.subscription.updated':
      await handleSubscriptionUpdate(event.data.object);
      break;
    default:
      console.log(`Unhandled event type: ${event.type}`);
  }

  // Always return 200 quickly — process async if needed
  return NextResponse.json({ received: true });
}
```

**Webhook rules:**
- Always verify signatures before processing
- Return `200` quickly — do heavy processing async
- Use `req.text()` not `req.json()` — signature verification needs raw body
- Log unhandled event types (don't error on them — providers add new events)
- Implement idempotency — webhooks can be sent multiple times

### Step 8: Generate TypeScript Interfaces

Produce type definitions that match the API contract:

```typescript
// types/api/organizations.ts

// Request types (match Zod schemas)
export interface CreateOrganizationRequest {
  name: string;
  slug?: string;
  plan?: 'free' | 'starter' | 'professional' | 'enterprise';
}

export interface UpdateOrganizationRequest {
  name?: string;
  settings?: Partial<OrganizationSettings>;
}

// Response types (match database + API transforms)
export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan: 'free' | 'starter' | 'professional' | 'enterprise';
  createdAt: string; // ISO 8601
  updatedAt: string;
}

export interface OrganizationWithMembers extends Organization {
  members: OrganizationMember[];
  memberCount: number;
}

// List response with pagination
export interface OrganizationListResponse {
  data: Organization[];
  meta: {
    total: number;
    page: number;
    limit: number;
  };
}
```

**Type generation rules:**
- Request types match Zod schemas (single source of truth)
- Response types match database models + any API transforms (e.g., `snake_case` → `camelCase`)
- Use `string` for dates in API types (ISO 8601 format over the wire)
- Export all types from a barrel file: `types/api/index.ts`

### Step 9: Complete Route Handler Template

Full boilerplate for a standard CRUD route:

```typescript
// app/api/organizations/[orgId]/projects/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { getAuthContext, verifyOrgAccess } from '@/lib/auth';
import { apiSuccess, apiError } from '@/lib/api-response';
import { db } from '@/lib/db';

// --- Validation Schemas ---
const createProjectSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
});

const listQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  status: z.enum(['draft', 'active', 'archived']).optional(),
});

// --- GET /api/organizations/[orgId]/projects ---
export async function GET(
  req: NextRequest,
  { params }: { params: { orgId: string } }
) {
  try {
    const auth = await getAuthContext(req);
    if (!auth) return apiError('Authentication required', 401);

    const access = await verifyOrgAccess(auth.userId, params.orgId);
    if (!access) return apiError('Access denied', 403);

    const query = listQuerySchema.safeParse(
      Object.fromEntries(new URL(req.url).searchParams)
    );
    if (!query.success) return apiError('Invalid query', 422, query.error.flatten());

    const { page, limit, status } = query.data;
    const offset = (page - 1) * limit;

    const [projects, total] = await Promise.all([
      db.projects.list({ orgId: params.orgId, status, limit, offset }),
      db.projects.count({ orgId: params.orgId, status }),
    ]);

    return NextResponse.json({
      data: projects,
      meta: { total, page, limit },
    });
  } catch (error) {
    console.error('GET /projects failed:', error);
    return apiError('Internal server error', 500);
  }
}

// --- POST /api/organizations/[orgId]/projects ---
export async function POST(
  req: NextRequest,
  { params }: { params: { orgId: string } }
) {
  try {
    const auth = await getAuthContext(req);
    if (!auth) return apiError('Authentication required', 401);

    const access = await verifyOrgAccess(auth.userId, params.orgId);
    if (!access) return apiError('Access denied', 403);
    if (access.role === 'viewer') return apiError('Insufficient permissions', 403);

    const body = await req.json();
    const parsed = createProjectSchema.safeParse(body);
    if (!parsed.success) return apiError('Validation failed', 422, parsed.error.flatten());

    const project = await db.projects.create({
      ...parsed.data,
      organizationId: params.orgId,
      createdBy: auth.userId,
    });

    return apiSuccess(project, 201);
  } catch (error) {
    console.error('POST /projects failed:', error);
    return apiError('Internal server error', 500);
  }
}
```

**Output summary:**

```
🔌 API Designer — Routes Complete

Feature: [name]
Routes: [count] endpoints across [count] resource groups

Route Table:
  Method  Path                                Auth   Status
  GET     /api/organizations                   ✅    List
  POST    /api/organizations                   ✅    Create
  GET     /api/organizations/[orgId]           ✅+O  Detail
  ...

Files to create:
  - app/api/organizations/route.ts
  - app/api/organizations/[orgId]/route.ts
  - app/api/organizations/[orgId]/projects/route.ts
  - lib/validations/organizations.ts (Zod schemas)
  - types/api/organizations.ts (TypeScript interfaces)

Zod schemas: [count] request validators
Type definitions: [count] interfaces
Webhooks: [count] with signature verification
Rate-limited routes: [count]
```

## Level History

- **Lv.1** — Base: Route structure design, auth guard chain (getAuthContext + verifyOrgAccess), Zod validation, consistent response format, HTTP status codes, rate limiting, webhook signature verification, TypeScript interfaces, full CRUD handler template. Based on AdminStack API patterns. (Origin: MemStack Pro v3.2, Mar 2026)
