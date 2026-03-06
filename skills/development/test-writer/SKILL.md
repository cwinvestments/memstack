---
name: test-writer
description: "Use when the user says 'write tests', 'add tests', 'test coverage', 'unit tests', 'integration tests', or wants to generate test files for existing code."
---

# 🧪 Test Writer — Comprehensive Test Generation
*Analyze code for untested paths and generate unit, integration, and component tests with proper mocking and edge case coverage.*

## Activation

When this skill activates, output:

`🧪 Test Writer — Generating tests for your codebase...`

| Context | Status |
|---------|--------|
| **User says "write tests", "add tests", "test coverage"** | ACTIVE |
| **User wants unit, integration, or component tests** | ACTIVE |
| **User mentions mocking, edge cases, or test strategy** | ACTIVE |
| **User wants to plan a refactor (tests are part of it)** | DORMANT — see refactor-planner |
| **User wants to plan a database migration** | DORMANT — see migration-planner |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Target code**: Which files, modules, or features need tests?
- **Language/framework**: What's the tech stack? (Node/Jest, Python/pytest, React/Vitest, etc.)
- **Test runner**: What test framework is already configured?
- **Existing tests**: Are there any tests already? What's the coverage?
- **Priority areas**: What's most critical to test? (business logic, API routes, UI components)
- **External dependencies**: What needs mocking? (databases, APIs, file system)

### Step 2: Analyze Critical Paths

Identify the most important code paths to test:

| Priority | Code Path | Type | Risk | Coverage |
|----------|-----------|------|------|----------|
| 🔴 Critical | [business logic / payment flow / auth] | Unit | High — bugs here lose money | None |
| 🟡 Important | [API routes / data transforms] | Integration | Medium — breaks user flows | Partial |
| 🟢 Standard | [utility functions / helpers] | Unit | Low — isolated, simple | None |
| 🟢 Standard | [UI components / forms] | Component | Medium — user-facing | None |

**Critical path detection rules:**
- Handles money or sensitive data → 🔴 Critical
- Called by 5+ other modules → 🔴 Critical
- Has complex branching (3+ conditions) → 🟡 Important
- Pure function with clear inputs/outputs → 🟢 Standard (but easy to test)
- Recently had bugs → 🔴 Critical regardless of type

### Step 3: Generate Unit Tests

For utility functions and business logic:

**Test structure:**
```javascript
describe('[ModuleName]', () => {
  describe('[functionName]', () => {
    // Happy path
    it('should [expected behavior] when [condition]', () => {
      const result = functionName(validInput);
      expect(result).toEqual(expectedOutput);
    });

    // Edge cases
    it('should handle null input gracefully', () => {
      expect(() => functionName(null)).not.toThrow();
    });

    it('should return empty array when given empty input', () => {
      const result = functionName([]);
      expect(result).toEqual([]);
    });

    // Boundary values
    it('should handle maximum allowed value', () => {
      const result = functionName(MAX_VALUE);
      expect(result).toBeDefined();
    });

    it('should handle minimum allowed value', () => {
      const result = functionName(MIN_VALUE);
      expect(result).toBeDefined();
    });

    // Error states
    it('should throw ValidationError for invalid input', () => {
      expect(() => functionName(invalidInput)).toThrow(ValidationError);
    });
  });
});
```

**Test naming convention:**
- `describe` block: Module or class name
- Nested `describe`: Function or method name
- `it` block: `should [behavior] when [condition]`
- Never use `test` as a verb in descriptions

**Coverage targets per function type:**
| Function Type | Min Coverage | Key Cases |
|---------------|-------------|-----------|
| Pure functions | 100% | All branches, boundary values |
| Business logic | 90% | Happy path, every error branch |
| Data transforms | 95% | Null, empty, malformed, large |
| Validators | 100% | Valid, each invalid case |

### Step 4: Generate Integration Tests

For API routes and service interactions:

```javascript
describe('[Route/Service] Integration', () => {
  // Setup
  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterEach(async () => {
    await cleanupTestData();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  describe('POST /api/[resource]', () => {
    it('should create resource and return 201', async () => {
      const response = await request(app)
        .post('/api/resource')
        .send(validPayload)
        .set('Authorization', `Bearer ${testToken}`);

      expect(response.status).toBe(201);
      expect(response.body).toMatchObject({
        id: expect.any(String),
        ...validPayload,
      });
    });

    it('should return 400 for invalid payload', async () => {
      const response = await request(app)
        .post('/api/resource')
        .send(invalidPayload)
        .set('Authorization', `Bearer ${testToken}`);

      expect(response.status).toBe(400);
      expect(response.body.error).toBeDefined();
    });

    it('should return 401 without authentication', async () => {
      const response = await request(app)
        .post('/api/resource')
        .send(validPayload);

      expect(response.status).toBe(401);
    });
  });
});
```

**Integration test categories:**
| Category | What to Test | Setup Needed |
|----------|-------------|--------------|
| API routes | Request/response cycle, status codes, body shape | Test server, auth tokens |
| Database queries | CRUD operations, constraints, transactions | Test database, seed data |
| Service-to-service | Function calls across module boundaries | Mocked external services |
| Middleware | Auth, validation, rate limiting, error handling | Request mocks |

### Step 5: Generate Component Tests

For React/UI components (user-event based):

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from './ComponentName';

describe('<ComponentName />', () => {
  const defaultProps = {
    onSubmit: vi.fn(),
    initialValue: '',
  };

  it('renders with default props', () => {
    render(<ComponentName {...defaultProps} />);
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('calls onSubmit with form data when submitted', async () => {
    const user = userEvent.setup();
    render(<ComponentName {...defaultProps} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.click(screen.getByRole('button', { name: /submit/i }));

    expect(defaultProps.onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
    });
  });

  it('shows validation error for invalid input', async () => {
    const user = userEvent.setup();
    render(<ComponentName {...defaultProps} />);

    await user.type(screen.getByLabelText(/email/i), 'not-an-email');
    await user.click(screen.getByRole('button', { name: /submit/i }));

    expect(screen.getByText(/valid email/i)).toBeInTheDocument();
    expect(defaultProps.onSubmit).not.toHaveBeenCalled();
  });

  it('disables submit button while loading', () => {
    render(<ComponentName {...defaultProps} isLoading={true} />);
    expect(screen.getByRole('button', { name: /submit/i })).toBeDisabled();
  });
});
```

**Component testing rules:**
- Query by role, label, or text — never by class name or test ID (unless necessary)
- Use `userEvent` over `fireEvent` — simulates real user behavior
- Test user-visible behavior, not implementation details
- Don't test styling — test that elements appear/disappear
- Mock child components only when they have side effects

### Step 6: Mock External Dependencies

Provide mocking patterns for common services:

**Database (Supabase/Prisma/Drizzle):**
```javascript
// Mock Supabase client
vi.mock('@/lib/supabase', () => ({
  supabase: {
    from: vi.fn(() => ({
      select: vi.fn().mockReturnThis(),
      insert: vi.fn().mockReturnThis(),
      update: vi.fn().mockReturnThis(),
      delete: vi.fn().mockReturnThis(),
      eq: vi.fn().mockReturnThis(),
      single: vi.fn().mockResolvedValue({ data: mockData, error: null }),
    })),
    auth: {
      getUser: vi.fn().mockResolvedValue({ data: { user: mockUser }, error: null }),
    },
  },
}));
```

**External APIs (Stripe, SendGrid, etc.):**
```javascript
// Mock Stripe
vi.mock('stripe', () => ({
  default: vi.fn(() => ({
    customers: {
      create: vi.fn().mockResolvedValue({ id: 'cus_test' }),
      retrieve: vi.fn().mockResolvedValue(mockCustomer),
    },
    checkout: {
      sessions: {
        create: vi.fn().mockResolvedValue({ url: 'https://checkout.stripe.com/test' }),
      },
    },
  })),
}));
```

**Fetch/HTTP:**
```javascript
// Mock global fetch
const mockFetch = vi.fn();
global.fetch = mockFetch;

beforeEach(() => {
  mockFetch.mockResolvedValue({
    ok: true,
    json: async () => mockResponse,
    status: 200,
  });
});
```

**Mocking principles:**
- Mock at the boundary — mock the external service, not your wrapper
- Reset mocks between tests (`vi.clearAllMocks()` in `afterEach`)
- Test both success and failure responses from mocks
- Use `mockResolvedValueOnce` for sequence-dependent tests

### Step 7: Edge Case Coverage

Systematic edge case checklist per input type:

| Input Type | Edge Cases to Test |
|-----------|-------------------|
| **String** | Empty `""`, whitespace `"  "`, very long (10000 chars), special chars `<>&"'`, unicode `🎉`, SQL injection `'; DROP TABLE--` |
| **Number** | Zero `0`, negative `-1`, float `0.1 + 0.2`, `NaN`, `Infinity`, max safe integer |
| **Array** | Empty `[]`, single item `[x]`, very large (10000 items), nested arrays, duplicate items |
| **Object** | Empty `{}`, missing required keys, extra unknown keys, nested nulls |
| **Date** | Past date, future date, midnight, DST transition, invalid date string, epoch `0` |
| **Boolean** | `true`, `false`, truthy `1`, falsy `0`, `null`, `undefined` |
| **File** | Empty file, very large file, wrong format, corrupted data, missing file |
| **Auth** | No token, expired token, invalid token, wrong permissions, admin vs user |

**Error state testing:**
```javascript
describe('error handling', () => {
  it('should handle network timeout', async () => {
    mockFetch.mockRejectedValue(new Error('ETIMEOUT'));
    await expect(fetchData()).rejects.toThrow('ETIMEOUT');
  });

  it('should handle malformed JSON response', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => { throw new SyntaxError('Unexpected token'); },
    });
    await expect(fetchData()).rejects.toThrow();
  });

  it('should handle concurrent access', async () => {
    const results = await Promise.all([
      processItem('item-1'),
      processItem('item-2'),
      processItem('item-3'),
    ]);
    expect(results).toHaveLength(3);
  });
});
```

### Step 8: Test File Organization

Structure test files to mirror source code:

```
src/
  utils/
    formatDate.ts         →  __tests__/utils/formatDate.test.ts
  services/
    paymentService.ts     →  __tests__/services/paymentService.test.ts
  api/
    routes/
      users.ts            →  __tests__/api/routes/users.test.ts
  components/
    UserForm.tsx          →  __tests__/components/UserForm.test.tsx
```

**Or colocated pattern:**
```
src/
  utils/
    formatDate.ts
    formatDate.test.ts
  components/
    UserForm.tsx
    UserForm.test.tsx
```

Follow whichever pattern the project already uses. If no convention exists, recommend colocated.

### Step 9: Output

Present the complete test suite:

```
━━━ TEST SUITE: [Module/Feature Name] ━━━━━

── COVERAGE ANALYSIS ──────────────────────
Critical paths identified: [count]
Current coverage: [%]
Target coverage: [%]

── UNIT TESTS ─────────────────────────────
File: [test file path]
Tests: [count]
[complete test file code]

── INTEGRATION TESTS ──────────────────────
File: [test file path]
Tests: [count]
[complete test file code]

── COMPONENT TESTS ────────────────────────
File: [test file path]
Tests: [count]
[complete test file code]

── MOCKS ──────────────────────────────────
[mock setup files]

── EDGE CASES COVERED ─────────────────────
[checklist of edge cases per input type]

── RUN INSTRUCTIONS ───────────────────────
Command: [test run command]
Watch mode: [watch command]
Coverage report: [coverage command]
```

## Inputs
- Target code files or modules
- Language and test framework
- Current coverage level
- Priority areas (business logic, API, UI)
- External dependencies to mock

## Outputs
- Critical path analysis with priority ranking
- Unit tests for utility functions and business logic
- Integration tests for API routes with setup/teardown
- Component tests using user-event patterns
- Mock configurations for external dependencies (Supabase, Stripe, APIs)
- Systematic edge case coverage (null, empty, boundary, error states)
- Complete test files with setup, assertions, and cleanup
- Test naming convention: describe/it with clear behavior descriptions

## Level History

- **Lv.1** — Base: Critical path analysis, unit test generation with boundary/edge cases, integration tests with setup/teardown, component tests (user-event based), mock patterns for Supabase/Stripe/fetch, systematic edge case checklist per input type, test file organization, describe/it naming convention. (Origin: MemStack v3.2, Mar 2026)
