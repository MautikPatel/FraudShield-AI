# Database Design

**Project:** FraudShield AI  
**Product:** Real-Time Payment Fraud Detection Platform

---

# Purpose

This document defines the database structure for FraudShield AI.

The database is designed to:

- Store payment transactions
- Store fraud detection results
- Record triggered fraud rules
- Save AI-generated investigation summaries
- Support dashboard analytics

The design prioritizes simplicity for the MVP while remaining extensible for future enterprise-scale enhancements.

---

# Database Technology

| Property | Value |
|----------|-------|
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migration Tool | Alembic |
| Primary Key | UUID |
| Timestamp | UTC |

---

# Database Design Principles

| Principle | Description |
|-----------|-------------|
| Single Source of Truth | Every fraud investigation starts from a transaction. |
| Normalized Design | Avoid duplicate data where practical. |
| Auditability | Preserve fraud decisions for future analysis. |
| Scalability | Allow future partitioning and indexing. |
| Extensibility | New fraud rules and AI features can be added without redesigning the schema. |

---

# Entity Relationship Diagram (ERD)

```text
                     +----------------------+
                     |     Transactions     |
                     +----------------------+
                      | Transaction ID (PK)
                      |
          +-----------+-----------+
          |           |           |
          ▼           ▼           ▼
+----------------+ +-------------------+ +----------------------+
| Fraud Scores   | | Triggered Rules   | | AI Explanations      |
+----------------+ +-------------------+ +----------------------+
        |
        ▼
+----------------------+
| Fraud Investigations |
+----------------------+
```

---

# Database Tables

## 1. Transactions

Stores all incoming payment transactions.

| Column | Type | Description |
|---------|------|-------------|
| transaction_id | UUID | Primary Key |
| card_number | VARCHAR | Masked card number |
| merchant_name | VARCHAR | Merchant |
| merchant_category | VARCHAR | Merchant type |
| amount | DECIMAL | Transaction amount |
| currency | VARCHAR | Currency |
| country | VARCHAR | Transaction country |
| device_id | VARCHAR | Device identifier |
| transaction_time | TIMESTAMP | Transaction timestamp |
| status | VARCHAR | Processed / Failed |

---

## 2. Fraud Scores

Stores fraud prediction results.

| Column | Type |
|---------|------|
| score_id | UUID |
| transaction_id | UUID (FK) |
| rule_score | DECIMAL |
| ml_score | DECIMAL |
| final_score | DECIMAL |
| risk_level | VARCHAR |
| prediction | VARCHAR |
| created_at | TIMESTAMP |

---

## 3. Triggered Rules

Stores every fraud rule triggered for a transaction.

| Column | Type |
|---------|------|
| rule_result_id | UUID |
| transaction_id | UUID (FK) |
| rule_name | VARCHAR |
| rule_weight | INTEGER |
| triggered | BOOLEAN |
| created_at | TIMESTAMP |

---

## 4. AI Explanations

Stores AI-generated investigation summaries.

| Column | Type |
|---------|------|
| explanation_id | UUID |
| transaction_id | UUID (FK) |
| summary | TEXT |
| recommendation | TEXT |
| generated_at | TIMESTAMP |

---

## 5. Fraud Investigations

Tracks analyst review status.

| Column | Type |
|---------|------|
| investigation_id | UUID |
| transaction_id | UUID (FK) |
| assigned_to | VARCHAR |
| investigation_status | VARCHAR |
| resolution | VARCHAR |
| reviewed_at | TIMESTAMP |

---

# Table Relationships

| Parent | Child | Relationship |
|---------|-------|--------------|
| Transactions | Fraud Scores | One-to-One |
| Transactions | Triggered Rules | One-to-Many |
| Transactions | AI Explanations | One-to-One |
| Transactions | Fraud Investigations | One-to-One |

---

# Transaction Lifecycle

```text
Transaction Created
        │
        ▼
Saved to Database
        │
        ▼
Rule Evaluation
        │
        ▼
ML Prediction
        │
        ▼
Risk Score Generated
        │
        ▼
AI Explanation Created
        │
        ▼
Analyst Investigation (Optional)
```

---

# Indexing Strategy

| Table | Index |
|--------|-------|
| Transactions | transaction_id |
| Transactions | transaction_time |
| Transactions | country |
| Transactions | merchant_name |
| Fraud Scores | final_score |
| Triggered Rules | transaction_id |
| Fraud Investigations | investigation_status |

---

# Future Enhancements

The following entities are intentionally excluded from the MVP and can be introduced in future phases:

- Users
- Roles & Permissions (RBAC)
- Fraud Rule Configuration
- Audit Logs
- Notification History
- Model Versioning
- Feature Store

---

# Design Decisions

| Decision | Reason |
|----------|--------|
| UUID Primary Keys | Globally unique identifiers suitable for distributed systems |
| Separate Fraud Score Table | Keeps detection results independent from transaction data |
| Separate Triggered Rules Table | Supports multiple rule matches per transaction |
| AI Explanations Stored Separately | Enables explanation regeneration without modifying transaction records |
| Investigation Table | Allows future analyst workflows without changing core transaction data |

---

# Product Manager's Perspective

The database design reflects the product workflow rather than the implementation details.

Every fraud investigation begins with a transaction, and all supporting information—risk scores, triggered rules, AI explanations, and investigation outcomes—is linked back to that transaction.

This approach keeps the data model intuitive, minimizes redundancy, and provides a solid foundation for analytics, reporting, and future enterprise capabilities.

---

# What's Next?

The final Phase 1 document defines the REST APIs that connect the frontend, backend, and AI services.

➡️ **Next Document:** `04_API_Specification.md`