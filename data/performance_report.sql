SELECT
    position,
    AVG(performance) AS performance
FROM table_name
GROUP BY position
ORDER BY performance DESC;