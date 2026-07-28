# Product Scope

**Project:** FraudShield AI  
**Product:** Real-Time Payment Fraud Detection Platform

---

# Why Product Scope Matters

Every successful product starts with clear boundaries.

Without a defined scope, projects quickly become overloaded with features, timelines slip, and the MVP loses focus.

FraudShield AI is intentionally designed using an **MVP-first approach**—building the smallest valuable product before expanding into enterprise-scale capabilities.

---

# Scope Overview

| Category | Focus |
|----------|-------|
| In Scope | Features included in the MVP |
| Out of Scope | Features intentionally excluded from the MVP |
| Future Scope | Planned enhancements after MVP validation |

---

# MVP Goals

The first version of FraudShield AI aims to answer one simple question:

> **Can we detect, explain, and visualize fraudulent payment transactions in real time using a combination of business rules and machine learning?**

Everything included in the MVP supports this goal.

---

# In Scope (MVP)

## Transaction Processing

- Payment transaction simulator
- Real-time transaction ingestion
- Transaction validation
- Transaction history

---

## Fraud Detection

- Rule-based fraud detection
- Configurable fraud rules
- Risk score generation
- Fraud classification
- High-risk transaction identification

---

## Machine Learning

- XGBoost fraud prediction model
- Feature engineering
- Model inference
- Risk probability calculation

---

## AI Investigation Assistant

- AI-generated fraud explanations
- Investigation summaries
- Triggered rule explanations
- Risk factor summaries

---

## Dashboard & Analytics

- Live fraud dashboard
- Transaction analytics
- Fraud trends
- Risk score distribution
- Rule trigger analytics
- Key performance indicators (KPIs)

---

## Backend Services

- REST APIs
- FastAPI backend
- PostgreSQL integration
- Configuration management
- Logging

---

# Out of Scope (MVP)

The following features are intentionally excluded from the first release.

## Infrastructure

- Kubernetes
- Multi-region deployment
- Auto Scaling
- High Availability Clustering

---

## Streaming

- Apache Kafka
- Apache Flink
- Apache Spark Streaming

---

## Security

- Single Sign-On (SSO)
- OAuth
- Multi-Factor Authentication
- Enterprise Identity Management

---

## Advanced AI

- Online Model Retraining
- AutoML
- Multi-model Ensemble Learning
- Reinforcement Learning

---

## Fraud Operations

- Case Management System
- Analyst Assignment Workflow
- Escalation Management
- Workflow Automation

---

## Notifications

- Email Alerts
- SMS Alerts
- Slack Notifications
- Microsoft Teams Integration

---

# Future Scope

Once the MVP is validated, FraudShield AI can evolve with additional capabilities.

## Platform

- Kafka Event Streaming
- Redis Caching
- Docker Compose
- Kubernetes
- Cloud Deployment

---

## AI

- SHAP Explainability
- LLM-powered Fraud Investigation Chat
- Continuous Learning
- Model Monitoring

---

## Fraud Intelligence

- Account Takeover Detection
- Identity Fraud Detection
- Merchant Risk Monitoring
- Behavioral Biometrics
- AML Detection

---

## Operations

- Rule Management Portal
- Analyst Work Queue
- Fraud Case Management
- Investigation Workflow

---

# MVP Feature Summary

| Module | Included |
|---------|-----------|
| Transaction Simulator | Yes |
| Rule Engine | Yes |
| ML Fraud Detection | Yes |
| Risk Scoring | Yes |
| AI Investigation Assistant | Yes |
| Dashboard | Yes |
| REST APIs | Yes |
| PostgreSQL | Yes |
| Authentication | No |
| Kafka | No |
| Kubernetes | No |
| Cloud Deployment | No |

---

# Scope Boundaries

The MVP is intentionally focused on validating the core fraud detection workflow.

```
Transaction
      │
      ▼
Rule Engine
      │
      ▼
Machine Learning
      │
      ▼
Risk Score
      │
      ▼
AI Explanation
      │
      ▼
Dashboard
```

Everything outside this workflow is considered future scope.

---

# Scope Decisions

| Decision | Reason |
|----------|--------|
| Build one ML model | Validate business value before comparing multiple models |
| No Kafka in MVP | Reduce infrastructure complexity while proving the concept |
| No Authentication | Focus on fraud detection capabilities before enterprise security |
| Streamlit Dashboard | Faster development and validation |
| PostgreSQL | Simple, reliable, and sufficient for MVP data storage |

---

# Product Manager's Perspective

One of the most common reasons software projects fail is uncontrolled scope growth.

Every additional feature increases development effort, testing, maintenance, and operational complexity.

For FraudShield AI, success is not measured by the number of features delivered.

Success is measured by delivering a focused MVP that solves a real business problem, validates product assumptions, and creates a strong foundation for future enhancements.

Building less—but building the right things—is a deliberate product strategy.

---

# What's Next?

Now that we've defined what belongs in the MVP, the next step is to document the assumptions and constraints that will guide product and technical decisions throughout development.

➡️ **Next Document:** `07_Assumptions_And_Constraints.md`