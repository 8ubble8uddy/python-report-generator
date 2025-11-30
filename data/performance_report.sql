SELECT
    position,
    AVG(performance) AS performance
FROM report_table
GROUP BY position
ORDER BY performance DESC;