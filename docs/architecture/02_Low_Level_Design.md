# Low-Level Design (LLD)

**Project:** FraudShield AI  
**Product:** Real-Time Payment Fraud Detection Platform

---

# Purpose

The Low-Level Design (LLD) describes the internal structure of FraudShield AI and explains how each module collaborates to process a payment transaction from ingestion to fraud decision.

Unlike the High-Level Architecture, which focuses on major system components, this document details the responsibilities, interactions, and data flow between internal modules.

---

# Design Principles

| Principle | Description |
|-----------|-------------|
| Single Responsibility | Every module performs one primary function. |
| Loose Coupling | Components communicate through well-defined interfaces. |
| High Cohesion | Related functionality stays within the same module. |
| Reusability | Business logic is reusable across APIs and services. |
| Testability | Modules can be tested independently. |

---

# Project Structure

```text
fraudshield-ai/
│
├── app/
│   ├── api/
│   ├── services/
│   ├── rules/
│   ├── ml/
│   ├── ai/
│   ├── database/
│   ├── repositories/
│   ├── models/
│   ├── schemas/
│   ├── simulator/
│   ├── core/
│   └── utils/
│
├── datasets/
├── docs/
├── tests/
└── requirements.txt
```

---

# Module Responsibilities

| Module | Responsibility |
|---------|----------------|
| api | REST endpoints |
| services | Business orchestration |
| simulator | Generate payment transactions |
| rules | Rule-based fraud detection |
| ml | Machine learning inference |
| ai | Fraud explanation generation |
| repositories | Database operations |
| database | Database connection and configuration |
| models | Database entities |
| schemas | Request and response models |
| core | Configuration and logging |
| utils | Shared helper functions |

---

# Request Processing Flow

```text
Client
   │
   ▼
API Layer
   │
   ▼
Service Layer
   │
   ├──────────────┐
   ▼              ▼
Rule Engine   ML Engine
   │              │
   └──────┬───────┘
          ▼
 Risk Scoring Engine
          │
          ▼
 AI Investigation
          │
          ▼
 Repository Layer
          │
          ▼
 PostgreSQL
```

---

# API Layer

### Responsibilities

- Receive HTTP requests
- Validate input
- Call service layer
- Return API responses

### Does NOT

- Execute business logic
- Access the database directly
- Perform fraud calculations

---

# Service Layer

The Service Layer coordinates the entire fraud detection workflow.

### Responsibilities

- Orchestrate fraud detection
- Coordinate modules
- Handle business rules
- Return final fraud decision

### Services

| Service | Purpose |
|----------|---------|
| TransactionService | Process transactions |
| FraudDetectionService | Execute fraud analysis |
| DashboardService | Prepare dashboard data |
| AIService | Generate explanations |

---

# Rule Engine

### Responsibilities

- Execute fraud rules
- Record triggered rules
- Calculate rule score

### Example Rules

- High Amount
- Velocity Check
- New Device
- High-Risk Country
- Blacklisted Merchant

---

# Machine Learning Module

### Responsibilities

- Load trained model
- Perform feature engineering
- Predict fraud probability
- Return confidence score

---

# Risk Scoring Engine

### Responsibilities

- Combine rule score
- Combine ML prediction
- Calculate overall risk
- Assign risk category

### Risk Levels

| Score | Level |
|--------|-------|
| 0–39 | Low |
| 40–69 | Medium |
| 70–100 | High |

---

# AI Investigation Assistant

### Responsibilities

- Summarize fraud decision
- Explain triggered rules
- Highlight risk factors
- Recommend next actions

### Example Output

```text
Transaction TXN-10025 was classified as HIGH RISK.

Reasons:
• High transaction amount
• Multiple transactions within 2 minutes
• High-risk country

Recommended Action:
Review before approval.
```

---

# Repository Layer

### Responsibilities

- Insert transactions
- Retrieve history
- Store fraud scores
- Query dashboard data

Repositories isolate database access from business logic.

---

# Database Layer

Stores:

- Transactions
- Fraud Scores
- Triggered Rules
- AI Explanations
- Dashboard Metrics

The database should never contain business logic.

---

# Error Handling Strategy

| Error | Handling |
|--------|----------|
| Invalid Request | Return HTTP 400 |
| Missing Transaction | Return HTTP 404 |
| Database Failure | Log error and return HTTP 500 |
| ML Prediction Failure | Log error and fall back to rule-based decision (future enhancement) |
| AI Explanation Failure | Return fraud decision without AI explanation |

---

# Logging Strategy

The application should log:

- API requests
- Fraud decisions
- Triggered rules
- ML predictions
- Database errors
- AI failures

Logs should support troubleshooting without exposing sensitive payment information.

---

# Sequence Diagram

```text
Client
   │
   ▼
FastAPI
   │
   ▼
TransactionService
   │
   ├────────────┐
   ▼            ▼
Rules      ML Model
   │            │
   └─────┬──────┘
         ▼
 Risk Engine
         ▼
 AI Assistant
         ▼
 Repository
         ▼
 PostgreSQL
         ▼
 Response
```

---

# Design Decisions

| Decision | Reason |
|----------|--------|
| Service Layer | Keeps APIs lightweight and business logic centralized |
| Repository Pattern | Simplifies database access and testing |
| Modular Rule Engine | Makes adding new fraud rules straightforward |
| AI as Independent Module | Allows explanation logic to evolve separately from detection logic |
| Separate Schemas | Prevents API contracts from depending on database models |

---

# Product Manager's Perspective

The internal design should make it easy to introduce new fraud rules, replace machine learning models, or enhance AI capabilities without affecting unrelated components.

This modular approach supports faster feature delivery, easier testing, and lower maintenance costs while keeping the platform adaptable to future business requirements.

---

# What's Next?

The next document defines the database schema, relationships, and data model that support FraudShield AI.

➡️ **Next Document:** `03_Database_Design.md`