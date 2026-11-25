-- =====================================================================
-- Project: Customer Churn & Retention Analytics
-- Script 01: Database & Table Schema Setup
-- Database: MySQL 8.0+
-- Description: Creates the analytical tables, constraints, and indexes
-- =====================================================================

CREATE DATABASE IF NOT EXISTS churn_analytics_db;
USE churn_analytics_db;

DROP TABLE IF EXISTS customer_churn;

CREATE TABLE customer_churn (
    customer_id VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    senior_citizen TINYINT NOT NULL,
    partner VARCHAR(5) NOT NULL,
    dependents VARCHAR(5) NOT NULL,
    tenure_months INT NOT NULL,
    phone_service VARCHAR(5) NOT NULL,
    multiple_lines VARCHAR(25) NOT NULL,
    internet_service VARCHAR(25) NOT NULL,
    online_security VARCHAR(25) NOT NULL,
    online_backup VARCHAR(25) NOT NULL,
    device_protection VARCHAR(25) NOT NULL,
    tech_support VARCHAR(25) NOT NULL,
    streaming_tv VARCHAR(25) NOT NULL,
    streaming_movies VARCHAR(25) NOT NULL,
    contract_type VARCHAR(20) NOT NULL,
    paperless_billing VARCHAR(5) NOT NULL,
    payment_method VARCHAR(35) NOT NULL,
    monthly_charges DECIMAL(10, 2) NOT NULL,
    total_charges DECIMAL(10, 2) NOT NULL,
    usage_frequency_logins INT NOT NULL,
    support_tickets INT NOT NULL,
    last_interaction_days INT NOT NULL,
    churn_risk_score DECIMAL(5, 2) NOT NULL,
    risk_tier VARCHAR(15) NOT NULL,
    churn VARCHAR(5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_contract (contract_type),
    INDEX idx_risk_tier (risk_tier),
    INDEX idx_churn (churn),
    INDEX idx_tenure (tenure_months)
);

-- Verification
DESCRIBE customer_churn;
