---
name: memstack-deployment-ci-cd-pipeline
description: "Use this skill when the user says 'CI/CD', 'GitHub Actions', 'pipeline', 'continuous integration', 'continuous deployment', 'ci-cd-pipeline', 'automate deploys', or needs to set up automated build, test, and deployment pipelines. Do NOT use for one-time manual deployments."
version: 1.0.0
license: "Proprietary — MemStack™ Pro by CW Affiliate Investments LLC. See LICENSE.txt"
---

# 🔄 CI/CD Pipeline — Continuous Integration & Deployment
*Detect project type and generate a complete CI/CD pipeline with lint, test, build, deploy stages, rollback strategy, and environment management.*

## Activation

When this skill activates, output:

`🔄 CI/CD Pipeline — Designing your pipeline...`

| Context | Status |
|---------|--------|
| **User says "CI/CD", "pipeline", "GitHub Actions"** | ACTIVE |
| **User wants automated testing and deployment** | ACTIVE |
| **User mentions branch strategy, deploy gates, or rollbacks** | ACTIVE |
| **User wants Docker setup (CI/CD is secondary)** | DORMANT — see docker-setup |
| **User wants server provisioning (not pipeline)** | DORMANT — see hetzner-setup |
| **User wants to deploy to a specific platform only** | DORMANT — see railway-deploy or netlify-deploy |

## Protocol

### Step 1: Gather Inputs

Ask the user for:
- **Project type**: Node.js, Python, Go, Rust, monorepo?
- **Testing framework**: Jest, Vitest, Pytest, Go test?
- **Deployment target**: Vercel, Railway, Netlify, Hetzner VPS, AWS, Docker registry?
- **Current CI/CD**: Any existing pipeline, or starting from scratch?
- **Branch strategy**: Trunk-based, GitFlow, or custom?
- **Team size**: Solo dev, small team, or large team?

### Step 2: Detect Project & Recommend Platform

Auto-detect from project files and recommend CI/CD platform:

| Project Signal | Platform Recommendation | Reason |
|---------------|------------------------|--------|
| `.github/` exists | GitHub Actions | Already on GitHub, native integration |
| `vercel.json` or Next.js | Vercel (auto-deploy) + GitHub Actions (CI) | Vercel handles deploy, GHA handles testing |
| `railway.json` | Railway (auto-deploy) + GitHub Actions (CI) | Railway handles deploy, GHA handles testing |
| `netlify.toml` | Netlify (auto-deploy) + GitHub Actions (CI) | Netlify handles deploy, GHA handles testing |
| Dockerfile present | GitHub Actions → Docker registry → deploy | Full control pipeline |
| Monorepo (`packages/`) | GitHub Actions with matrix/path filters | Need per-package CI |
| Self-hosted server | GitHub Actions → SSH deploy | Push-based deployment |

**Default recommendation: GitHub Actions** — free for public repos, 2,000 min/month for private.

### Step 3: Design Pipeline Stages

Define the stage sequence:

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  LINT   │──→│  TEST   │──→│  BUILD  │──→│ DEPLOY  │──→│ VERIFY  │
│         │   │         │   │         │   │         │   │         │
│ ESLint  │   │ Unit    │   │ Compile │   │ Push to │   │ Health  │
│ Prettier│   │ Integ.  │   │ Bundle  │   │ target  │   │ Smoke   │
│ Types   │   │ E2E     │   │ Docker  │   │ env     │   │ Rollback│
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
     │              │              │              │              │
  Fail fast    Gate: block     Artifacts      Env-specific    Auto-rollback
  < 1 min      if < 80%       cached         secrets         on failure
```

**Stage details:**

| Stage | Trigger | Failure Action | Duration Target |
|-------|---------|---------------|-----------------|
| **Lint** | Every push, every PR | Block merge | < 1 min |
| **Test** | Every push, every PR | Block merge | < 5 min |
| **Build** | PR merge to main/develop | Block deploy | < 3 min |
| **Deploy** | Build passes on target branch | Alert + rollback | < 2 min |
| **Verify** | After deploy completes | Auto-rollback | < 1 min |

### Step 4: Branch Strategy

**Recommended: Simplified GitFlow**

```
main (production)
  ├── develop (staging)
  │     ├── feature/add-auth
  │     ├── feature/dashboard
  │     └── fix/login-bug
  └── hotfix/critical-fix (→ main + develop)
```

| Branch | Deploys To | CI Runs | Auto-Deploy? |
|--------|-----------|---------|-------------|
| `feature/*` | — | Lint + Test | No |
| `develop` | Staging | Lint + Test + Build + Deploy | Yes |
| `main` | Production | Lint + Test + Build + Deploy | Yes (or manual gate) |
| `hotfix/*` | — | Lint + Test | No (merge to main to deploy) |

**Branch protection rules:**
```
main:
  - Require PR review (1+ approvals)
  - Require status checks (lint, test, build)
  - No force push
  - No direct push

develop:
  - Require status checks (lint, test)
  - Allow direct push (for solo devs)
  - No force push
```

### Step 5: Environment Variable Management

```
── ENVIRONMENT VARIABLES ──────────────────

Three environments with escalating secrets:

LOCAL (.env.local — never committed):
  DATABASE_URL=postgresql://localhost:5432/app_dev
  API_KEY=dev_test_key
  NODE_ENV=development

STAGING (GitHub Secrets / platform env):
  DATABASE_URL=[staging DB connection string]
  API_KEY=[staging API key]
  NODE_ENV=staging

PRODUCTION (GitHub Secrets / platform env):
  DATABASE_URL=[production DB connection string]
  API_KEY=[production API key]
  NODE_ENV=production
```

**Secret management rules:**
- Never hardcode secrets in pipeline config
- Use GitHub Environments for per-branch secrets
- Use `GITHUB_TOKEN` for GitHub operations (auto-provided)
- Rotate secrets quarterly
- Audit secret access in GitHub Settings → Secrets → Audit log

**GitHub Environments setup:**
```
Repository → Settings → Environments:
  staging:
    Secrets: DATABASE_URL, API_KEY
    Deployment branches: develop

  production:
    Secrets: DATABASE_URL, API_KEY
    Deployment branches: main
    Required reviewers: [team member] (optional gate)
```

### Step 6: Generate Pipeline Config

**GitHub Actions — Node.js project:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck  # If TypeScript

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-report
          path: coverage/

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/
      # Platform-specific deploy step here
      # Option A: Railway
      # - uses: bervProject/railway-deploy@main
      #   with:
      #     railway_token: ${{ secrets.RAILWAY_TOKEN }}
      # Option B: SSH deploy to VPS
      # - uses: appleboy/ssh-action@v1
      #   with:
      #     host: ${{ secrets.SERVER_HOST }}
      #     username: deploy
      #     key: ${{ secrets.SSH_PRIVATE_KEY }}
      #     port: 2222
      #     script: |
      #       cd /opt/app && git pull && npm ci --production && pm2 restart all

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/
      # Same deploy pattern as staging but with production env

  verify:
    name: Verify Deployment
    runs-on: ubuntu-latest
    needs: [deploy-staging, deploy-production]
    if: always() && (needs.deploy-staging.result == 'success' || needs.deploy-production.result == 'success')
    steps:
      - name: Health check
        run: |
          URL="${{ github.ref == 'refs/heads/main' && secrets.PRODUCTION_URL || secrets.STAGING_URL }}"
          for i in 1 2 3 4 5; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL/health")
            if [ "$STATUS" = "200" ]; then
              echo "Health check passed"
              exit 0
            fi
            echo "Attempt $i: HTTP $STATUS — retrying in 10s..."
            sleep 10
          done
          echo "Health check failed after 5 attempts"
          exit 1
```

**GitHub Actions — Python project:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy .

  test:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: pytest --cov --cov-report=xml
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb

  build-and-deploy:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4
      # Docker build + push or direct deploy
```

### Step 7: Deployment Rollback Strategy

**Automated rollback on failed health check:**

```yaml
  rollback:
    name: Rollback on Failure
    runs-on: ubuntu-latest
    needs: verify
    if: failure()
    steps:
      - name: Rollback deployment
        run: |
          echo "Deployment verification failed — rolling back"
          # Option A: Revert to previous Docker image
          # docker pull $REGISTRY/app:previous && docker tag $REGISTRY/app:previous $REGISTRY/app:latest
          # Option B: Railway rollback
          # railway rollback
          # Option C: Git revert + redeploy
          # git revert HEAD --no-edit && git push
      - name: Notify team
        run: |
          curl -X POST "${{ secrets.SLACK_WEBHOOK }}" \
            -H 'Content-Type: application/json' \
            -d '{"text":"🔴 Deployment rolled back — health check failed on ${{ github.ref }}"}'
```

**Rollback strategies by deployment target:**

| Target | Rollback Method | Speed | Data Safety |
|--------|----------------|-------|------------|
| **Vercel** | Instant rollback in dashboard or CLI | Instant | Safe — immutable deploys |
| **Railway** | `railway rollback` or dashboard | Instant | Safe — previous deploy preserved |
| **Netlify** | Deploy previous build in dashboard | Instant | Safe — immutable deploys |
| **Docker** | Tag previous image as `latest`, restart | Seconds | Safe — images preserved |
| **VPS/PM2** | `git revert` + `pm2 restart` | Minutes | Check DB migrations first |
| **Kubernetes** | `kubectl rollout undo` | Seconds | Check DB migrations first |

**Database migration caution:**
- If the deploy includes DB migrations, rollback is complex
- Always write reversible migrations (`up` + `down`)
- Test `down` migration before deploying `up`
- Consider: deploy DB migration separately from code deploy

### Step 8: Notifications

**Slack notification on deploy:**

```yaml
  notify:
    name: Notify
    runs-on: ubuntu-latest
    needs: [deploy-staging, deploy-production, verify]
    if: always()
    steps:
      - name: Send Slack notification
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        run: |
          if [ "${{ needs.verify.result }}" = "success" ]; then
            EMOJI="✅"
            STATUS="succeeded"
          else
            EMOJI="🔴"
            STATUS="failed"
          fi
          curl -X POST "$SLACK_WEBHOOK" \
            -H 'Content-Type: application/json' \
            -d "{
              \"text\": \"${EMOJI} Deploy ${STATUS}\",
              \"blocks\": [
                {
                  \"type\": \"section\",
                  \"text\": {
                    \"type\": \"mrkdwn\",
                    \"text\": \"${EMOJI} *Deploy ${STATUS}*\nBranch: \`${{ github.ref_name }}\`\nCommit: \`${{ github.sha }}\`\nBy: ${{ github.actor }}\"
                  }
                }
              ]
            }"
```

**Alternative notification channels:**
- **GitHub Actions built-in**: Email on failure (Settings → Notifications)
- **Discord webhook**: Same curl pattern, different payload format
- **PagerDuty**: For production failures that need on-call response

### Step 9: Output

Present the complete CI/CD configuration:

```
━━━ CI/CD PIPELINE ━━━━━━━━━━━━━━━━━━━━━━━
Project: [name]
Platform: GitHub Actions
Deploy target: [platform]
Branch strategy: [strategy]

── PIPELINE STAGES ────────────────────────
Lint → Test → Build → Deploy → Verify
[stage diagram with timing]

── BRANCH STRATEGY ────────────────────────
[branch → environment mapping]
[protection rules]

── ENVIRONMENT VARIABLES ──────────────────
[per-environment secret setup]

── PIPELINE CONFIG ────────────────────────
[complete .github/workflows/ci-cd.yml]

── ROLLBACK STRATEGY ──────────────────────
[per-target rollback method]
[database migration caution]

── NOTIFICATIONS ──────────────────────────
[Slack/Discord/email setup]

── SETUP CHECKLIST ────────────────────────
[ ] Create .github/workflows/ directory
[ ] Add pipeline YAML file
[ ] Configure GitHub Environments (staging, production)
[ ] Add secrets to each environment
[ ] Set branch protection rules
[ ] Configure notification webhook
[ ] Test pipeline with a feature branch PR
[ ] Verify staging deploy on develop merge
[ ] Verify production deploy on main merge
```

## Inputs
- Project type and language
- Testing framework
- Deployment target
- Branch strategy preference
- Team size
- Existing CI/CD (if any)

## Outputs
- Pipeline stage design with timing targets
- Branch strategy with protection rules
- Environment variable management per stage
- Complete CI/CD config file (GitHub Actions YAML)
- Deployment rollback strategy per target
- Notification setup (Slack, Discord, email)
- Setup checklist for first-time configuration

## Level History

- **Lv.1** — Base: Auto-detect project type, 5-stage pipeline (lint/test/build/deploy/verify), GitHub Actions configs for Node.js and Python, simplified GitFlow branch strategy, environment variable management with GitHub Environments, automated rollback on health check failure, Slack notifications, setup checklist. (Origin: MemStack v3.2, Mar 2026)
