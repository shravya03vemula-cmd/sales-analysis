-- ============================================================
-- SALES ANALYSIS PROJECT
-- Dataset: Superstore Sales
-- ============================================================

CREATE TABLE IF NOT EXISTS orders (
    order_id        VARCHAR(20),
    order_date      DATE,
    ship_date       DATE,
    ship_mode       VARCHAR(30),
    customer_id     VARCHAR(20),
    customer_name   VARCHAR(100),
    segment         VARCHAR(20),
    country         VARCHAR(50),
    city            VARCHAR(50),
    state           VARCHAR(50),
    region          VARCHAR(20),
    product_id      VARCHAR(20),
    category        VARCHAR(30),
    sub_category    VARCHAR(30),
    product_name    VARCHAR(200),
    sales           DECIMAL(10,2),
    quantity        INT,
    discount        DECIMAL(4,2),
    profit          DECIMAL(10,2)
);

-- 1. REVENUE BY YEAR
SELECT
    YEAR(order_date)                                        AS year,
    COUNT(DISTINCT order_id)                                AS total_orders,
    ROUND(SUM(sales), 2)                                    AS total_revenue,
    ROUND(SUM(profit), 2)                                   AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)    AS profit_margin_pct
FROM orders
GROUP BY YEAR(order_date)
ORDER BY year;

-- 2. MONTHLY REVENUE TREND
SELECT
    DATE_FORMAT(order_date, '%Y-%m')    AS month,
    ROUND(SUM(sales), 2)                AS revenue,
    ROUND(SUM(profit), 2)               AS profit,
    COUNT(DISTINCT order_id)            AS orders
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

-- 3. REVENUE BY CATEGORY
SELECT
    category,
    ROUND(SUM(sales), 2)                                    AS revenue,
    ROUND(SUM(profit), 2)                                   AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)    AS profit_margin_pct
FROM orders
GROUP BY category
ORDER BY revenue DESC;

-- 4. SUB-CATEGORY BREAKDOWN
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2)                                    AS revenue,
    ROUND(SUM(profit), 2)                                   AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)    AS profit_margin_pct
FROM orders
GROUP BY category, sub_category
ORDER BY category, revenue DESC;

-- 5. TOP 10 PRODUCTS BY REVENUE
SELECT
    product_name,
    category,
    ROUND(SUM(sales), 2)    AS revenue,
    ROUND(SUM(profit), 2)   AS profit,
    SUM(quantity)           AS units_sold
FROM orders
GROUP BY product_name, category
ORDER BY revenue DESC
LIMIT 10;

-- 6. REGIONAL PERFORMANCE
SELECT
    region,
    ROUND(SUM(sales), 2)                                    AS revenue,
    ROUND(SUM(profit), 2)                                   AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)    AS profit_margin_pct,
    COUNT(DISTINCT customer_id)                             AS unique_customers
FROM orders
GROUP BY region
ORDER BY revenue DESC;

-- 7. TOP 10 STATES
SELECT
    state,
    region,
    ROUND(SUM(sales), 2)        AS revenue,
    ROUND(SUM(profit), 2)       AS profit,
    COUNT(DISTINCT order_id)    AS orders
FROM orders
GROUP BY state, region
ORDER BY revenue DESC
LIMIT 10;

-- 8. CUSTOMER SEGMENT ANALYSIS
SELECT
    segment,
    COUNT(DISTINCT customer_id)                             AS unique_customers,
    ROUND(SUM(sales), 2)                                    AS revenue,
    ROUND(SUM(profit), 2)                                   AS profit,
    ROUND(SUM(sales) / COUNT(DISTINCT customer_id), 2)      AS revenue_per_customer,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)    AS profit_margin_pct
FROM orders
GROUP BY segment
ORDER BY revenue DESC;

-- 9. DISCOUNT IMPACT
SELECT
    CASE
        WHEN discount = 0               THEN '0% no discount'
        WHEN discount BETWEEN 0.01 AND 0.1  THEN '1-10%'
        WHEN discount BETWEEN 0.11 AND 0.2  THEN '11-20%'
        WHEN discount BETWEEN 0.21 AND 0.3  THEN '21-30%'
        ELSE '30% plus'
    END                                         AS discount_bucket,
    COUNT(*)                                    AS orders,
    ROUND(SUM(sales), 2)                        AS revenue,
    ROUND(SUM(profit), 2)                       AS profit,
    ROUND(AVG(profit / NULLIF(sales,0))*100, 2) AS avg_margin_pct
FROM orders
GROUP BY discount_bucket
ORDER BY MIN(discount);

-- 10. SHIPPING MODE PERFORMANCE
SELECT
    ship_mode,
    COUNT(DISTINCT order_id)                            AS orders,
    ROUND(SUM(sales), 2)                                AS revenue,
    ROUND(AVG(DATEDIFF(ship_date, order_date)), 1)      AS avg_ship_days
FROM orders
GROUP BY ship_mode
ORDER BY orders DESC;