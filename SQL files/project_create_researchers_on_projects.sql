create view researchers_on_projects AS (
  SELECT r.researcher_id, CONCAT(first_name, ' ', last_name) fullname, title
  from project p, researcher r
  WHERE p.supervisor_id = r.researcher_id

  UNION

  select r.researcher_id, CONCAT(first_name, ' ', last_name) fullname, project_title
  from works_on w, researcher r 
  where w.researcher_id = r.researcher_id
);
