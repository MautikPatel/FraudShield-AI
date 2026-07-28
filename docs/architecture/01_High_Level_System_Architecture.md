# High-Level System Architecture

**Project:** FraudShield AI  
**Product:** Real-Time Payment Fraud Detection Platform

---

# Purpose

The High-Level System Architecture provides an overview of the major components that make up FraudShield AI and explains how they interact to deliver real-time fraud detection.

The architecture is intentionally modular, allowing individual components to evolve independently while maintaining a simple and maintainable MVP.

---

# Architecture Principles

The platform is designed around the following principles.

| Principle | Description |
|------------|-------------|
| Modular Design | Each component has a single responsibility. |
| API-First | All business capabilities are exposed through REST APIs. |
| Explainable AI | Every fraud decision should include supporting evidence. |
| Scalable by Design | The MVP uses lightweight components while allowing future enterprise scaling. |
| Separation of Concerns | Business rules, ML, AI, database, and UI remain independent modules. |

---

# High-Level Architecture

```text
                        FraudShield AI

                        +----------------+
                        |   Dashboard    |
                        |   (Streamlit)  |
                        +-------+--------+
                                |
                                |
                    REST API Requests
                                |
                                ▼
+--------------------------------------------------------------+
|                     FastAPI Backend                          |
|--------------------------------------------------------------|
| Transaction API | Fraud API | Dashboard API | Health API     |
+-----------------+-----------+---------------+----------------+
          |                |               |
          |                |               |
          ▼                ▼               ▼
+----------------+  +----------------+  +----------------+
| Rule Engine    |  | ML Model       |  | AI Assistant   |
|                |  | (XGBoost)      |  | (LLM)          |
+-------+--------+  +--------+-------+  +-------+--------+
        |                    |                    |
        +----------+---------+--------------------+
                   |
                   ▼
          +----------------------+
          | Risk Scoring Engine  |
          +----------+-----------+
                     |
                     ▼
             +---------------+
             | PostgreSQL DB |
             +---------------+
```

---

# Component Overview

| Component | Responsibility |
|-----------|----------------|
| Streamlit Dashboard | Displays KPIs, fraud trends, and investigation results |
| FastAPI Backend | Receives requests and coordinates business logic |
| Rule Engine | Detects known fraud patterns using configurable rules |
| ML Model | Predicts fraud probability |
| Risk Scoring Engine | Combines rule results and ML predictions |
| AI Investigation Assistant | Generates human-readable fraud explanations |
| PostgreSQL | Stores transactions, scores, and investigation data |

---

# End-to-End Request Flow

```text
Payment Transaction
        │
        ▼
FastAPI Backend
        │
        ├──────────────┐
        ▼              ▼
Rule Engine      ML Fraud Model
        │              │
        └──────┬───────┘
               ▼
      Risk Scoring Engine
               │
               ▼
 AI Investigation Assistant
               │
               ▼
       PostgreSQL Database
               │
               ▼
 Dashboard & REST APIs
```

---

# Component Responsibilities

## 1. Transaction Processing

Receives incoming payment transactions, validates required fields, and forwards them for fraud analysis.

**Input**

- Payment transaction

**Output**

- Validated transaction

---

## 2. Rule Engine

Applies predefined business rules to detect known fraud patterns.

Example rules include:

- High Amount
- Velocity Check
- High-Risk Country
- New Device
- Blacklisted Merchant

**Output**

- Triggered fraud rules

---

## 3. Machine Learning Model

Evaluates transaction characteristics using an XGBoost model.

**Output**

- Fraud probability
- Prediction confidence

---

## 4. Risk Scoring Engine

Combines business rules and ML predictions into a unified fraud risk score.

Possible outcomes:

- Low Risk
- Medium Risk
- High Risk

---

## 5. AI Investigation Assistant

Transforms technical fraud signals into analyst-friendly explanations.

Example:

> Transaction flagged due to unusually high amount, rapid transaction frequency, and elevated model risk score.

---

## 6. Dashboard

Provides operational visibility through:

- Fraud KPIs
- Live transaction monitoring
- Risk score distribution
- Fraud trends
- Rule analytics

---

## 7. Database

Stores:

- Transactions
- Fraud scores
- Triggered rules
- AI explanations
- Dashboard metrics

---

# Architecture Decisions

| Decision | Reason |
|----------|--------|
| FastAPI | Lightweight, asynchronous, and easy to extend |
| PostgreSQL | Reliable relational database with strong SQL support |
| XGBoost | Well-suited for structured fraud datasets |
| Streamlit | Rapid dashboard development for MVP |
| Modular Architecture | Enables future scaling without major redesign |

---

# Future Evolution

The architecture has been designed to evolve without changing the overall workflow.

### Phase 2

- Improved fraud rules
- Additional ML features
- Enhanced dashboard

### Phase 3

- Explainable AI
- Investigation Chat
- Analyst feedback loop

### Phase 4

- Kafka Event Streaming
- Docker
- RBAC
- CI/CD Pipeline
- Cloud Deployment
- Monitoring

---

# Architecture Benefits

| Benefit | Value |
|----------|-------|
| Modular | Easier maintenance and testing |
| Scalable | Ready for future distributed architecture |
| Explainable | Supports analyst investigations |
| Extensible | New fraud rules and models can be added independently |
| Maintainable | Clear separation of responsibilities |

---

# Product Manager's Perspective

The MVP architecture prioritizes clarity, modularity, and business value over infrastructure complexity.

Rather than introducing technologies solely because they are industry trends, the design focuses on proving the core fraud detection workflow first.

As transaction volume and business needs grow, components such as event streaming, authentication, monitoring, and cloud deployment can be introduced with minimal architectural disruption.

---

# What's Next?

The next document zooms into each component and describes the internal modules, interactions, and responsibilities in greater detail.

➡️ **Next Document:** `02_Low_Level_Design.md`