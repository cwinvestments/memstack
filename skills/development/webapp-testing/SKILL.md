---
name: memstack-development-webapp-testing
description: "Use when the user says 'write browser tests', 'test this page', 'playwright test', 'e2e test', 'end to end test', 'browser test', 'test the UI', or needs Playwright-based browser testing for a web application. Do NOT use for unit tests, API tests, or non-browser testing."
version: 1.0.0
---

# Webapp Testing — Writing browser tests...
*Produces Playwright end-to-end tests that verify real user flows in a browser.*

## Activation

| Trigger | Status |
|---------|--------|
| User says "write browser tests" or "playwright test" | ACTIVE |
| User says "test this page" or "e2e test" | ACTIVE |
| User says "test the UI" or "browser test" | ACTIVE |
| User wants unit tests or API tests | NOT this skill — use standard test patterns |
| User wants load testing | NOT this skill |

## Context Guard

- Do NOT use for unit tests (Jest, Vitest without browser)
- Do NOT use for API-only testing (use curl/fetch patterns)
- Do NOT use for performance benchmarking
- This skill ONLY produces Playwright browser tests

## Steps

### Step 1: Assess the target

Determine what to test:

| Parameter | How to find | Example |
|-----------|-------------|---------|
| App URL | Check package.json scripts, .env, or ask | `http://localhost:3000` |
| Framework | Check package.json dependencies | Next.js, React, SvelteKit |
| Auth required? | Check for login pages, auth middleware | Yes/No |
| Key user flows | Ask or infer from routes | Sign up, checkout, search |

```bash
# Check if Playwright is already installed
cat package.json | grep -i playwright

# Check existing test structure
find . -name "*.spec.ts" -o -name "*.test.ts" | head -20
```

### Step 2: Set up Playwright (if not installed)

```bash
npm init playwright@latest
# or
pnpm add -D @playwright/test
npx playwright install
```

Confirm `playwright.config.ts` exists. If not, create with sensible defaults:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Step 3: Write tests for each user flow

Follow this structure per flow:

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test('should [expected behavior] when [action]', async ({ page }) => {
    // Arrange — navigate to the page
    await page.goto('/path');

    // Act — perform user actions
    await page.getByRole('button', { name: 'Submit' }).click();

    // Assert — verify the result
    await expect(page.getByText('Success')).toBeVisible();
  });
});
```

**Test writing rules:**
1. Use `getByRole`, `getByLabel`, `getByText` over CSS selectors — they survive refactors
2. One assertion per test where practical — clear failure messages
3. Name tests as user stories: "should show error when email is invalid"
4. Use `test.describe` to group related flows
5. Add `test.beforeEach` for shared navigation/auth setup
6. Never hardcode waits — use `expect` with auto-waiting or `waitForSelector`

### Step 4: Handle authentication flows

If the app requires login:

```typescript
// tests/e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('testpassword');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page).toHaveURL('/dashboard');

  // Save signed-in state
  await page.context().storageState({ path: '.auth/user.json' });
});
```

Add to `playwright.config.ts`:

```typescript
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'chromium',
    use: {
      ...devices['Desktop Chrome'],
      storageState: '.auth/user.json',
    },
    dependencies: ['setup'],
  },
],
```

### Step 5: Common test patterns

**Form validation:**
```typescript
test('should show validation errors for empty required fields', async ({ page }) => {
  await page.goto('/form');
  await page.getByRole('button', { name: 'Submit' }).click();
  await expect(page.getByText('Email is required')).toBeVisible();
});
```

**Navigation flow:**
```typescript
test('should navigate from landing to pricing', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'Pricing' }).click();
  await expect(page).toHaveURL('/pricing');
  await expect(page.getByRole('heading', { name: 'Pricing' })).toBeVisible();
});
```

**API response verification:**
```typescript
test('should load and display data', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.getByRole('table')).toBeVisible();
  await expect(page.locator('tbody tr')).toHaveCount(10);
});
```

### Step 6: Run and report

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/auth.spec.ts

# Run with UI mode for debugging
npx playwright test --ui

# Show HTML report
npx playwright show-report
```

Present results:

```
Playwright tests written:
- [N] test files covering [N] user flows
- Auth setup: [yes/no]
- Flows tested: [list]

Run with: npx playwright test
```

## Disambiguation

- "write browser tests" / "playwright test" / "e2e test" = Webapp Testing
- "write unit tests" / "jest test" / "vitest" = Standard test patterns (not this skill)
- "test the API" / "curl test" = API testing (not this skill)
- "verify my code" / "check this work" = Verify (not this skill)

## Level History

- **Lv.1** — Base: Playwright test generation with role-based selectors, auth flows, common patterns, CI-ready config. (Origin: MemStack v3.5, Apr 2026)
