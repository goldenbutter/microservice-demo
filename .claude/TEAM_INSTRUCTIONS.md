# 🤖 Agent Team Instructions — Microservice Demo

> **Created:** 2026-03-19  
> **Status:** READ-ONLY ANALYSIS PHASE (no modifications until requested)

---

## Team Structure

| Agent | Role | Domain |
|-------|------|--------|
| **Agent 1** | Backend Engineer | FastAPI microservices (`backend/`) |
| **Agent 2** | Frontend Engineer | Static UI (`frontend/`) |
| **Agent 3** | DevOps Engineer | Docker, Compose, Kubernetes (`Dockerfile`, `docker-compose.yml`, `k8s/`) |
| **Agent 4** | QA & Test Automation | Tests, quality, system-level validation |

---

## Ground Rules

### 🔒 Branch Policy
- **NEVER modify the `main` branch directly.**
- All future changes MUST be done in a **new feature branch**.
- Branch naming convention: `feature/<short-description>` or `agent/<agent-number>/<topic>`

### 📖 Current Phase: Analysis Only
- Each agent has read and analyzed the entire codebase within their domain.
- No rewrites or modifications are to be made until the user explicitly requests them.
- Agents document their findings internally and stay ready to act.

### 🤝 Collaboration Rules
- Agents may communicate to clarify architecture or verify assumptions.
- Each agent stays focused on their own domain but can request or share information.
- When a new feature is requested, each agent performs their part accordingly.
- Cross-domain changes (e.g., a new API endpoint that needs frontend + backend + k8s) require all relevant agents to coordinate.

---

## 🛠 Mission: SQLite Migration (Current Task)

> **Goal:** Upgrade the project from in-memory storage to a persistent SQLite database.

### Phase 3 Implementation Rules
- **Backend (Agent 1):** Use SQLAlchemy to bridge models and SQLite logic. Ensure table creation on startup.
- **Frontend (Agent 2):** Maintain API stability; ensure JSON schema remains unchanged.
- **DevOps (Agent 3):** Implement lightweight volume mounting for `app.db` persistence in both Docker Compose and Kubernetes.
- **QA (Agent 4):** Use `sqlite:///:memory:` for fast, automated tests that reset between runs.

---

## Agent Responsibilities

### Agent 1 — Backend Engineer (FastAPI)
- **Domain:** `backend/` (FastAPI, SQLAlchemy models, CRUD logic)
- **Phase 3:**
  - Add `sqlalchemy` to `requirements.txt`.
  - Migrate `database.py`, `models.py`, and `crud.py` to use SQLAlchemy.
  - Ensure all existing endpoints remain fully compatible.
  - Auto-create tables on startup.

### Agent 2 — Frontend Engineer (Static UI)
- **Domain:** `frontend/` (HTML, CSS, JS)
- **Phase 3:**
  - Verify UI stability with persistent backend.
  - Optionally add loading/error state indicators.

### Agent 3 — DevOps Engineer (Docker + K8s)
- **Domain:** `docker-compose.yml`, `k8s/`, `Dockerfile`
- **Phase 3:**
  - Define persistence strategy for the `app.db` file.
  - **Docker Compose:** Add a host-mounted volume for the data folder.
  - **Kubernetes:** Add a `PersistentVolumeClaim` (PVC) and mount it to the backend deployment.
  - Ensure correct folder permissions inside the container for SQLite write access.

### Agent 4 — QA & Test Automation
- **Domain:** Unit & Integration tests
- **Phase 3:**
  - Implement full test suite using `pytest`.
  - Set up a isolated in-memory SQLite database for testing.
  - Validate that the migration hasn't introduced regression bugs.

## 🛡️ Workflow Rulebook (Mandatory)

We follow a clean, production‑style workflow to ensure stability.

### 1. Branch Hierarchy
- **`main`**: Stable production branch. **NEVER** modify directly.
- **`claude-edit`**: Development branch. All our active work happens here.
- **`feature/*`**: Temporary branches for merging into `main`.

### 2. Implementation Cycle (The "Five Steps")

#### **Step 1 — Development (`claude-edit`)**
- Implement features, update code, and README.
- Reference GitHub Issues in commit messages (e.g., `#1`).
- **STOP** and notify the user when ready.

#### **Step 2 — Feature Branch Creation**
- Once confirmed, the agent will move code to a feature branch (e.g., `feature/sqlite-persistence-1.1`).
- Agent provides the Push command; **User** runs it.
- **STOP** and wait for User confirmation.

#### **Step 3 — Pull Request & Merge**
- **User** creates PR from `feature/*` → `main` in GitHub.
- **User** reviews and merges the PR.
- **User** confirms the merge to the Agent.
- Agent deletes the local feature branch.
- **STOP** and wait for User confirmation.

#### **Step 4 — Final Sync**
- Agents ensure `claude-edit` is synced with latest code.
- Agents stop and wait for the next feature request.

### 3. Communication Gates
- Agents **MUST** pause and wait for User approval at each checkpoint.
- If a User request violates these rules, Agents **MUST** remind the User and ask to override or follow.

---

## Final Goal (Updated)
A fully persistent microservice demo project where data survives restarts via a lightweight SQLite architecture, backed by a robust automated test suite, all deployed in the `claude-edit` branch.
