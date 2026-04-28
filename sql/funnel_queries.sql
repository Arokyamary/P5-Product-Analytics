-- FUNNEL: 5-step conversion by variant
WITH funnel AS (
SELECT variant,
COUNT(DISTINCT CASE WHEN event='landing' THEN user_id END) AS step1,
COUNT(DISTINCT CASE WHEN event='product_view' THEN user_id END) AS step2,
COUNT(DISTINCT CASE WHEN event='add_to_cart' THEN user_id END) AS step3,
COUNT(DISTINCT CASE WHEN event='checkout' THEN user_id END) AS step4,
COUNT(DISTINCT CASE WHEN event='purchase' THEN user_id END) AS step5
FROM events
GROUP BY variant
)
SELECT *, ROUND(step5 * 100.0 / step1, 2) AS overall_cvr_pct
FROM funnel;

-- COHORT RETENTION: Week-over-week
WITH cohort_week AS (
SELECT user_id,
DATE_TRUNC('week', MIN(ts)) AS cohort
FROM events
GROUP BY 1
),
weekly_activity AS (
SELECT e.user_id,
DATE_TRUNC('week', e.ts) AS activity_week,
c.cohort
FROM events e
JOIN cohort_week c USING (user_id)
)
SELECT cohort,
activity_week,
COUNT(DISTINCT user_id) AS retained_users,
ROUND(COUNT(DISTINCT user_id) * 100.0 /
FIRST_VALUE(COUNT(DISTINCT user_id)) OVER
(PARTITION BY cohort ORDER BY activity_week), 1) AS retention_pct
FROM weekly_activity
GROUP BY cohort, activity_week
ORDER BY cohort, activity_week;