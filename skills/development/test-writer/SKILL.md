---
name: memstack-development-test-writer
description: "Use this skill when the user says 'write tests', 'add tests', 'test coverage', 'unit tests', 'integration tests', 'component tests', 'mocking', 'edge cases', or needs to generate tests with proper mocking and edge case coverage. Do NOT use for refactoring plans or database migrations."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# Test Writer — Generating test suite...
*Generates comprehensive test suites with unit, integration, and e2e tests, proper mocking strategies, edge case coverage, naming conventions, and CI integration patterns.*

## Activation

When this skill activates, output:

`Test Writer — Generating test suite...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| User says "write tests", "add tests", "test coverage" | ACTIVE |
| User says "unit tests", "integration tests", "component tests", "e2e tests" | ACTIVE |
| User says "mocking", "edge cases", "test this function" | ACTIVE |
| User wants to refactor existing code | DORMANT — use Refactor Planner |
| User wants to change database schema | DORMANT — use Migration Planner |

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Testing implementation, not behavior" | Tests that break when you refactor internals are brittle. Test WHAT it does, not HOW. |
| "No edge cases" | Happy path tests catch 20% of bugs. Boundaries, nulls, empty inputs, and error paths catch the rest. |
| "Mocking everything" | Over-mocking creates tests that pass but don't catch real bugs. Mock boundaries, not internals. |
| "Test names like test1, test2" | Names should describe behavior: "returns empty array when no items match filter". Self-documenting tests. |
| "No test isolation" | Tests that depend on each other or shared state create flaky test suites that nobody trusts. |

## Protocol

### Step 1: Gather Test Requirements

If the user hasn't provided details, ask:

> 1. **Target** — what code needs tests? (function, class, module, API endpoint)
> 2. **Language/framework** — what tech stack? (JS/TS + Jest/Vitest, Python + pytest, Go, etc.)
> 3. **Test level** — unit, integration, e2e, or all three?
> 4. **Current coverage** — any existing tests? What percentage?
> 5. **Priority** — critical paths first, or comprehensive coverage?

### Step 2: Analyze the Code Under Test

Before writing tests, understand the target:

**Function/method analysis:**

| Property | Value |
|----------|-------|
| **Inputs** | [Parameters, types, optional/required] |
| **Outputs** | [Return type, side effects, thrown exceptions] |
| **Dependencies** | [External calls: DB, API, file system, other modules] |
| **State changes** | [What mutates: database records, cache, global state] |
| **Branching paths** | [Number of if/else/switch branches] |
| **Error conditions** | [What can fail and how it's handled] |

**Dependency map:**

```
[Target Function]
  ├── [Dependency 1] — mock? [Yes: external / No: pure]
  ├── [Dependency 2] — mock? [Yes: external / No: pure]
  └── [Dependency 3] — mock? [Yes: external / No: pure]
```

**Mock decision rule:**
- **Mock** external boundaries: databases, APIs, file system, network, time
- **Don't mock** pure functions, internal utilities, simple data transformations
- **Sometimes mock** sibling modules (mock for unit tests, real for integration)

### Step 3: Design Test Cases

**Coverage strategy — identify all test scenarios:**

**Happy path tests:**

| # | Scenario | Input | Expected Output |
|---|---------|-------|----------------|
| 1 | [Normal case with typical input] | [Input] | [Output] |
| 2 | [Normal case with different valid input] | [Input] | [Output] |

**Edge case tests:**

| # | Category | Scenario | Input | Expected Output |
|---|---------|---------|-------|----------------|
| 1 | **Boundaries** | Minimum valid value | [Input] | [Output] |
| 2 | **Boundaries** | Maximum valid value | [Input] | [Output] |
| 3 | **Boundaries** | Exactly at limit | [Input] | [Output] |
| 4 | **Empty** | Empty string / array / object | `""` / `[]` / `{}` | [Output] |
| 5 | **Null/Undefined** | Null input | `null` | [Output or error] |
| 6 | **Type coercion** | Unexpected type | `"123"` vs `123` | [Output] |
| 7 | **Large input** | Very large dataset | [X items] | [Output / perf] |
| 8 | **Unicode** | Special characters | `"café ñ 中文"` | [Output] |
| 9 | **Concurrent** | Race condition scenario | [Parallel calls] | [Consistent state] |

**Error path tests:**

| # | Error Condition | Input | Expected Behavior |
|---|----------------|-------|-------------------|
| 1 | Invalid input | [Bad input] | Throws [ErrorType] with message |
| 2 | Dependency failure | [DB timeout] | Returns fallback or propagates error |
| 3 | Permission denied | [Unauthorized] | Returns 403 / throws AuthError |
| 4 | Not found | [Missing resource] | Returns null or throws NotFoundError |

### Step 4: Write the Tests

**Test file naming conventions:**

| Framework | Convention | Example |
|-----------|----------|---------|
| Jest / Vitest | `[name].test.ts` or `[name].spec.ts` | `userService.test.ts` |
| pytest | `test_[name].py` | `test_user_service.py` |
| Go | `[name]_test.go` | `user_service_test.go` |
| JUnit | `[Name]Test.java` | `UserServiceTest.java` |

**Test naming conventions:**

| Style | Pattern | Example |
|-------|---------|---------|
| **Behavior-driven** | `should [expected] when [condition]` | `should return empty array when no items match filter` |
| **Given-When-Then** | `given [state] when [action] then [result]` | `given expired token when authenticating then throws AuthError` |
| **Method-focused** | `[method] — [scenario] — [expected]` | `calculateTotal — with discount — applies percentage reduction` |

**Test structure template (JavaScript/TypeScript):**

```typescript
describe('[ModuleName]', () => {
  // Setup shared across tests in this block
  let dependency: MockType;

  beforeEach(() => {
    dependency = createMock();
    // Reset state before each test
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('[methodName]', () => {
    // Happy path
    it('should [expected behavior] when [normal condition]', () => {
      // Arrange
      const input = { /* test data */ };
      dependency.method.mockResolvedValue(expectedData);

      // Act
      const result = targetMethod(input);

      // Assert
      expect(result).toEqual(expectedOutput);
    });

    // Edge case
    it('should [expected behavior] when [edge condition]', () => {
      // Arrange
      const input = { /* edge case data */ };

      // Act
      const result = targetMethod(input);

      // Assert
      expect(result).toEqual(edgeCaseOutput);
    });

    // Error path
    it('should throw [ErrorType] when [error condition]', () => {
      // Arrange
      const input = { /* invalid data */ };

      // Act & Assert
      expect(() => targetMethod(input)).toThrow(ErrorType);
    });
  });
});
```

**Test structure template (Python):**

```python
import pytest
from unittest.mock import Mock, patch

class TestModuleName:
    """Tests for [ModuleName]."""

    def setup_method(self):
        """Reset state before each test."""
        self.dependency = Mock()

    # Happy path
    def test_method_returns_expected_when_normal_input(self):
        """Should [expected behavior] when [condition]."""
        # Arrange
        input_data = {"key": "value"}
        self.dependency.method.return_value = expected_data

        # Act
        result = target_method(input_data)

        # Assert
        assert result == expected_output

    # Edge case
    def test_method_handles_empty_input(self):
        """Should [expected behavior] when input is empty."""
        result = target_method([])
        assert result == []

    # Error path
    def test_method_raises_error_when_invalid_input(self):
        """Should raise ValueError when [condition]."""
        with pytest.raises(ValueError, match="expected message"):
            target_method(invalid_input)
```

### Step 5: Mocking Strategy

**Mock patterns by dependency type:**

| Dependency | Mock Approach | Example |
|-----------|--------------|---------|
| **Database** | Mock repository/ORM layer | `jest.spyOn(db, 'query').mockResolvedValue(rows)` |
| **HTTP API** | Mock HTTP client or use MSW/nock | `nock('https://api.example.com').get('/users').reply(200, data)` |
| **File system** | Mock fs module or use memfs | `jest.mock('fs/promises')` |
| **Time/Date** | Fake timers | `jest.useFakeTimers(); jest.setSystemTime(new Date('2026-01-15'))` |
| **Random** | Seed or mock | `jest.spyOn(Math, 'random').mockReturnValue(0.5)` |
| **Environment** | Set/restore env vars | `process.env.NODE_ENV = 'test'` in beforeEach |
| **Third-party SDK** | Mock the client | `jest.mock('stripe', () => mockStripeClient)` |

**Mock verification patterns:**

```typescript
// Verify a dependency was called correctly
expect(mockDb.query).toHaveBeenCalledWith(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// Verify call count
expect(mockApi.fetch).toHaveBeenCalledTimes(1);

// Verify NOT called (important for caching tests)
expect(mockDb.query).not.toHaveBeenCalled();

// Verify call order (important for transaction tests)
const order = [];
mockDb.begin.mockImplementation(() => order.push('begin'));
mockDb.commit.mockImplementation(() => order.push('commit'));
// ... run test ...
expect(order).toEqual(['begin', 'commit']);
```

### Step 6: Integration & E2E Tests

**Integration test patterns:**

```typescript
describe('[Feature] Integration', () => {
  // Use real database (test instance), real logic, mock external APIs only
  let testDb: TestDatabase;

  beforeAll(async () => {
    testDb = await createTestDatabase();
    await testDb.migrate();
  });

  afterAll(async () => {
    await testDb.destroy();
  });

  beforeEach(async () => {
    await testDb.truncateAll(); // Clean state per test
  });

  it('should create user and send welcome email', async () => {
    // Arrange — mock only the email service (external boundary)
    const emailSpy = jest.spyOn(emailService, 'send').mockResolvedValue(true);

    // Act — use real DB, real validation, real business logic
    const user = await userService.register({
      email: 'test@example.com',
      name: 'Test User',
    });

    // Assert — verify real DB state + external call
    const dbUser = await testDb.query('SELECT * FROM users WHERE id = $1', [user.id]);
    expect(dbUser).toBeDefined();
    expect(emailSpy).toHaveBeenCalledWith(
      expect.objectContaining({ to: 'test@example.com' })
    );
  });
});
```

**E2E test patterns (API):**

```typescript
describe('POST /api/users', () => {
  it('should create a user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test User' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      email: 'test@example.com',
    });
  });

  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'not-an-email', name: 'Test' })
      .expect(400);

    expect(response.body.error).toContain('email');
  });

  it('should return 409 for duplicate email', async () => {
    // Create first user
    await request(app).post('/api/users').send({ email: 'dup@example.com', name: 'First' });

    // Attempt duplicate
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'dup@example.com', name: 'Second' })
      .expect(409);
  });
});
```

### Step 7: Coverage & CI Integration

**Coverage targets:**

| Level | Target | Rationale |
|-------|--------|-----------|
| **Critical paths** (auth, payments, data writes) | >90% | Bugs here = revenue loss or security issues |
| **Business logic** (services, domain) | >80% | Core value — must work correctly |
| **Utilities / helpers** | >70% | Important but lower risk |
| **UI components** | >60% | Visual testing often complements |
| **Overall project** | >75% | Healthy baseline |

**CI configuration template (GitHub Actions):**

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: npm ci
      - run: npm test -- --coverage

      - name: Check coverage thresholds
        run: |
          npx jest --coverage --coverageThreshold='{
            "global": {
              "branches": 75,
              "functions": 80,
              "lines": 80,
              "statements": 80
            }
          }'
```

**Test runner configuration:**

```json
// jest.config.js / vitest.config.ts
{
  "collectCoverageFrom": [
    "src/**/*.{ts,tsx}",
    "!src/**/*.d.ts",
    "!src/**/index.ts",
    "!src/**/*.stories.tsx"
  ],
  "coverageThresholds": {
    "global": {
      "branches": 75,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  }
}
```

**Pre-commit test check:**

```bash
# Only run tests related to changed files (fast feedback)
npx jest --onlyChanged
# or
npx vitest --changed
```

## Output Format

```markdown
# Test Suite — [Target Module/Function]

## Analysis
- **Target:** [What's being tested]
- **Dependencies:** [X] total ([X] mocked, [X] real)
- **Branching paths:** [X]

## Test Cases
### Unit Tests ([X] tests)
[Test code from Step 4]

### Edge Cases ([X] tests)
[Edge case tests from Step 3]

### Error Cases ([X] tests)
[Error path tests from Step 3]

### Integration Tests ([X] tests)
[Integration tests from Step 6, if requested]

## Coverage Summary
- Lines: [X]%
- Branches: [X]%
- Functions: [X]%

## CI Integration
[CI config from Step 7, if requested]
```

## Completion

```
Test Writer — Complete!

Target: [Module/function name]
Tests written: [X] total
  - Unit tests: [X]
  - Edge cases: [X]
  - Error cases: [X]
  - Integration tests: [X]
Mocked dependencies: [X]
Estimated coverage: [X]%

Next steps:
1. Run the test suite: [test command]
2. Check coverage report for uncovered branches
3. Add tests to CI pipeline (config provided above)
4. Add pre-commit hook to run related tests on save
5. Review and adjust coverage thresholds quarterly
```

## Level History

- **Lv.1** — Base: Code analysis template (inputs, outputs, dependencies, branches), 3-category test case design (happy path, edge cases, error paths), test templates for JS/TS and Python, 7 mock patterns by dependency type with verification, integration and E2E test patterns, coverage targets by code criticality, CI integration with GitHub Actions. (Origin: MemStack Pro v3.2, Mar 2026)
