CREATE view young_help AS (
SELECT researcher_id, fullname, COUNT(*) cnt
FROM young_researchers
GROUP BY researcher_id);