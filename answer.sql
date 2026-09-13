-- TYPE YOUR SQL QUERY BELOW


-- PART 1: Create a SQL query that maps out the daily average users before and after the feature change

-- PART 1:
-- Daily average users before and after the feature change.
-- Feature change date: 2018-06-02

WITH daily_users AS (
    SELECT
        date(login_timestamp, 'unixepoch') AS login_date,
        COUNT(DISTINCT user_id) AS users
    FROM login_history
    GROUP BY date(login_timestamp, 'unixepoch')
)
SELECT
    CASE
        WHEN login_date < '2018-06-02' THEN 'before'
        ELSE 'after'
    END AS period,
    AVG(users) AS daily_average_users
FROM daily_users
GROUP BY period;


-- PART 2: Create a SQL query that indicates the number of status changes by card
-- Number of status changes by card.

SELECT
    cardID AS card_id,
    COUNT(*) AS status_changes
FROM card_change_history
WHERE oldStatus IS NOT newStatus
GROUP BY cardID
ORDER BY cardID;






