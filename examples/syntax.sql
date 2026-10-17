-- PostgreSQL: CTEs, identifiers, functions, literals, and CASE.
WITH items(name, quantity, enabled) AS (
    VALUES
        ('ready', 42, TRUE),
        ('waiting', 2, FALSE),
        ('empty', 0, TRUE)
), totals AS (
    SELECT
        name,
        SUM(quantity) AS total,
        COUNT(*) FILTER (WHERE enabled) AS active_count
    FROM items
    GROUP BY name
)
SELECT
    name AS "Display name",
    total,
    CASE
        WHEN total >= 10 THEN 'busy'
        WHEN total = 0 THEN 'empty'
        ELSE 'waiting'
    END AS status,
    COALESCE(active_count, 0) AS active_count
FROM totals
WHERE name NOT LIKE 'test%'
ORDER BY total DESC
LIMIT 42;
