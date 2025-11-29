SELECT
    position,
    AVG(performance) AS performance
FROM performance
GROUP BY position
ORDER BY performance DESC;