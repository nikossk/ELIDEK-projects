CREATE VIEW young_researchers AS (
SELECT r.researcher_id, fullname, r.title, rr.birth_date,p.start_date, p.end_date
FROM researchers_on_projects r, project p, researcher rr
WHERE r.researcher_id = rr.researcher_id AND r.title = p.title 
	AND p.start_date < CURRENT_DATE AND p.end_date > CURRENT_DATE
	AND datediff(CURRENT_DATE, rr.birth_date) < 40 * 365
);
