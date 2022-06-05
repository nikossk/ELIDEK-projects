CREATE VIEW company_view (name, name_and_abbr, address, equity)
AS
SELECT 
	org.org_name,
	CONCAT(org.org_name, ' (', org.abbreviation, ')') name_and_abbr, 
	CONCAT(org.street, ' ', org.street_number, ',\n ', org.postal_code, ' ', org.city) address, 
	comp.equity
FROM 
	organisation org INNER JOIN company comp ON org.org_name = comp.name;
	
CREATE VIEW university_view (name, name_and_abbr, address, budget)
AS
SELECT 
	org.org_name,
	CONCAT(org.org_name, ' (', org.abbreviation, ')') name_and_abbr, 
	CONCAT(org.street, ' ', org.street_number, ',\n ', org.postal_code, ' ', org.city) address, 
	comp.budget
FROM 
	organisation org INNER JOIN university comp ON org.org_name = comp.name;
	
CREATE VIEW research_centre_view (name, name_and_abbr, address, budget_me, budget_pa)
AS
SELECT 
	org.org_name,
	CONCAT(org.org_name, ' (', org.abbreviation, ')') name_and_abbr, 
	CONCAT(org.street, ' ', org.street_number, ',\n ', org.postal_code, ' ', org.city) address, 
	comp.budget_me, comp.budget_pa
FROM 
	organisation org INNER JOIN research_centre comp ON org.org_name = comp.name;