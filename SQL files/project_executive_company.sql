CREATE VIEW executive_company AS (
	SELECT e.executive_id, CONCAT(first_name, ' ', last_name) fullname, c.org_name, p.amount
	FROM 
		project p INNER JOIN organisation c ON p.organisation_name = c.org_name
		INNER JOIN executive e ON e.executive_id = p.executive_id
	WHERE c.category = 'company'
);