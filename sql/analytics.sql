-- Superstore Analytics Queries

-- 1. Total revenue and profit by category
SELECT
    p.category,
    ROUND(SUM(f.sales)::numeric, 2)   AS total_revenue,
    ROUND(SUM(f.profit)::numeric, 2)  AS total_profit,
    ROUND(AVG(f.discount)::numeric * 100, 1) AS avg_discount_pct
FROM fact_orders f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 2. Monthly revenue trend
SELECT
    d.year,
    d.month,
    ROUND(SUM(f.sales)::numeric, 2) AS monthly_revenue,
    COUNT(DISTINCT f.order_id)      AS total_orders
FROM fact_orders f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 3. Top 10 customers by lifetime value
SELECT
    c.customer_name,
    c.segment,
    ROUND(SUM(f.sales)::numeric, 2)  AS lifetime_value,
    ROUND(SUM(f.profit)::numeric, 2) AS total_profit,
    COUNT(DISTINCT f.order_id)       AS total_orders
FROM fact_orders f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.customer_name, c.segment
ORDER BY lifetime_value DESC
LIMIT 10;

-- 4. Sales performance by region
SELECT
    r.region,
    r.state,
    ROUND(SUM(f.sales)::numeric, 2)  AS total_sales,
    ROUND(SUM(f.profit)::numeric, 2) AS total_profit,
    COUNT(DISTINCT f.order_id)       AS order_count
FROM fact_orders f
JOIN dim_region r ON f.region_id = r.region_id
GROUP BY r.region, r.state
ORDER BY total_sales DESC;

-- 5. Product ranking by revenue using window function
SELECT
    p.product_name,
    p.category,
    ROUND(SUM(f.sales)::numeric, 2) AS total_sales,
    RANK() OVER (
        PARTITION BY p.category
        ORDER BY SUM(f.sales) DESC
    ) AS rank_in_category
FROM fact_orders f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY p.category, rank_in_category
LIMIT 20;

-- 6. Quarter over quarter growth
SELECT
    d.year,
    d.quarter,
    ROUND(SUM(f.sales)::numeric, 2) AS quarterly_revenue,
    ROUND(SUM(f.sales)::numeric, 2) -
        LAG(ROUND(SUM(f.sales)::numeric, 2))
        OVER (ORDER BY d.year, d.quarter) AS revenue_growth
FROM fact_orders f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.quarter
ORDER BY d.year, d.quarter;