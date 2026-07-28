# API Specification

**Project:** FraudShield AI  
**Product:** Real-Time Payment Fraud Detection Platform

---

# Purpose

This document defines the REST APIs exposed by FraudShield AI.

The APIs enable communication between the dashboard, fraud detection engine, AI investigation assistant, and external systems.

The MVP follows REST principles and exchanges data using JSON.

---

# API Standards

| Property | Value |
|----------|-------|
| Architecture | REST |
| Data Format | JSON |
| Base URL | `/api/v1` |
| Authentication | Not required (MVP) |
| Content-Type | `application/json` |
| Response Format | JSON |

---

# API Overview

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/transactions` | Submit a payment transaction |
| GET | `/transactions` | Retrieve transactions |
| GET | `/transactions/{id}` | Retrieve transaction details |
| POST | `/fraud/analyze` | Analyze a transaction for fraud |
| GET | `/dashboard/summary` | Dashboard KPIs |
| GET | `/dashboard/trends` | Fraud trend analytics |
| GET | `/health` | Application health status |

---

# 1. Submit Transaction

## Endpoint

```http
POST /api/v1/transactions
```

### Description

Creates a new payment transaction and stores it in the system.

### Request

```json
{
  "merchant_name": "Amazon",
  "merchant_category": "Retail",
  "amount": 249.99,
  "currency": "USD",
  "country": "US",
  "device_id": "DEV-1001",
  "card_token": "CARD-9X2K7P"
}
```

### Success Response

```json
{
  "transaction_id": "TXN-100001",
  "status": "created",
  "message": "Transaction created successfully."
}
```

### Status Codes

| Code | Description |
|------|-------------|
| 201 | Transaction created |
| 400 | Invalid request |
| 500 | Internal server error |

---

# 2. Analyze Transaction

## Endpoint

```http
POST /api/v1/fraud/analyze
```

### Description

Performs fraud analysis using the rule engine, ML model, and risk scoring engine.

### Request

```json
{
  "transaction_id": "TXN-100001"
}
```

### Success Response

```json
{
  "transaction_id": "TXN-100001",
  "rule_score": 42,
  "ml_score": 81,
  "final_score": 73,
  "risk_level": "High",
  "fraud_detected": true
}
```

### Status Codes

| Code | Description |
|------|-------------|
| 200 | Analysis completed |
| 404 | Transaction not found |
| 500 | Internal server error |

---

# 3. Get Transaction Details

## Endpoint

```http
GET /api/v1/transactions/{transaction_id}
```

### Description

Returns detailed information for a single transaction.

### Success Response

```json
{
  "transaction_id": "TXN-100001",
  "merchant_name": "Amazon",
  "amount": 249.99,
  "risk_level": "High",
  "status": "Processed"
}
```

---

# 4. Get Transactions

## Endpoint

```http
GET /api/v1/transactions
```

### Description

Returns a paginated list of transactions.

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| page | Page number |
| limit | Number of records |
| risk_level | Filter by risk |
| merchant | Filter by merchant |

---

# 5. Dashboard Summary

## Endpoint

```http
GET /api/v1/dashboard/summary
```

### Description

Returns dashboard KPIs.

### Success Response

```json
{
  "total_transactions": 25000,
  "fraud_detected": 142,
  "fraud_rate": 0.57,
  "high_risk_transactions": 81
}
```

---

# 6. Fraud Trends

## Endpoint

```http
GET /api/v1/dashboard/trends
```

### Description

Returns fraud trends for dashboard visualizations.

### Success Response

```json
{
  "daily_transactions": [],
  "fraud_trend": [],
  "risk_distribution": []
}
```

---

# 7. Health Check

## Endpoint

```http
GET /api/v1/health
```

### Description

Verifies that the application is running.

### Success Response

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

# Standard Response Format

## Success

```json
{
  "success": true,
  "data": {},
  "message": "Request completed successfully."
}
```

## Error

```json
{
  "success": false,
  "error": "Validation Error",
  "message": "Merchant name is required."
}
```

---

# HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Resource created |
| 400 | Bad request |
| 401 | Unauthorized (Future) |
| 403 | Forbidden (Future) |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Validation error |
| 500 | Internal server error |

---

# Future API Enhancements

The following APIs are planned for future releases:

| Endpoint | Purpose |
|----------|---------|
| `/auth/login` | User authentication |
| `/users` | User management |
| `/rules` | Fraud rule management |
| `/investigations` | Case management |
| `/ai/chat` | Conversational fraud investigation |
| `/models` | ML model management |

---

# API Versioning Strategy

FraudShield AI uses URI versioning.

```text
/api/v1
/api/v2
```

This approach allows new versions to be introduced without breaking existing integrations.

---

# Product Manager's Perspective

The API design follows a resource-oriented approach that keeps endpoints simple, predictable, and easy to extend.

The MVP exposes only the APIs required to support transaction processing, fraud detection, and dashboard analytics. More advanced capabilities, such as authentication, investigation workflows, and rule management, are intentionally deferred until later phases to keep the initial release focused.

