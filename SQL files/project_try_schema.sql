DROP SCHEMA IF EXISTS project_try;
CREATE SCHEMA project_try;
USE project_try;

CREATE TABLE scientific_field (
	name VARCHAR(30) NOT NULL,
	PRIMARY KEY (name)
);

CREATE TABLE program (
	program_id SMALLINT NOT NULL AUTO_INCREMENT,
	name VARCHAR(150) NOT NULL,
	front_office VARCHAR(30) NOT NULL,
	PRIMARY KEY (program_id)
) AUTO_INCREMENT=41; 

CREATE TABLE executive (
	executive_id SMALLINT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(30) NOT NULL,
	last_name VARCHAR(30) NOT NULL,
	PRIMARY KEY (executive_id)
) AUTO_INCREMENT=21;

CREATE TABLE organisation (
	org_name VARCHAR(80) NOT NULL,
	abbreviation VARCHAR(15) NOT NULL,
	postal_code CHAR(5) NOT NULL,
	street VARCHAR(50) NOT NULL,
	street_number TINYINT UNSIGNED NOT NULL,
	city VARCHAR(20) NOT NULL,
	category VARCHAR(20) NOT NULL,	
	PRIMARY KEY (org_name),
	CHECK (category IN ('company',
				'university','research_centre')),
	CHECK(postal_code REGEXP '^[0-9]{5}$')
);

CREATE TABLE telephone (
	tel_number CHAR(10) NOT NULL,
	organisation_name VARCHAR(80) NOT NULL,
	PRIMARY KEY (tel_number),
	CONSTRAINT fkk_organisation_name 
		FOREIGN KEY (organisation_name)
		REFERENCES organisation (org_name) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
		CHECK(tel_number REGEXP '^[0-9]{10}$')
);

CREATE TABLE company (
	name VARCHAR(80) NOT NULL,
	equity NUMERIC(12,2) NOT NULL,
	PRIMARY KEY (NAME),
	CONSTRAINT fk_company_name 
		FOREIGN KEY (name)
		REFERENCES organisation (org_name) 
		ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE university (
	name VARCHAR(80) NOT NULL,
	budget NUMERIC(12,2) NOT NULL,
	PRIMARY KEY (NAME),
	CONSTRAINT fk_university_name 
		FOREIGN KEY (name)
		REFERENCES organisation (org_name) 
		ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE research_centre (
	name VARCHAR(80) NOT NULL,
	budget_me NUMERIC(12,2) NOT NULL,
	budget_pa NUMERIC(12,2) NOT NULL,
	PRIMARY KEY (NAME),
	CONSTRAINT fk_reasearch_centre_name 
		FOREIGN KEY (name)
		REFERENCES organisation (org_name) 
		ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE researcher (
	researcher_id SMALLINT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(30) NOT NULL,
	last_name VARCHAR(30) NOT NULL,
	sex CHAR(1) NOT NULL,
	birth_date DATE NOT NULL,
	employment_date DATE NOT NULL,
	organisation_name VARCHAR(80) NOT NULL,
	PRIMARY KEY (researcher_id),
	CONSTRAINT fk_organisation_name 
		FOREIGN KEY (organisation_name)
		REFERENCES organisation (org_name) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CHECK (sex IN ('m','f','o')),
	CHECK (employment_date < CURRENT_DATE),
	CHECK (DATEDIFF(employment_date, birth_date) >= 6574)
) AUTO_INCREMENT=151;

CREATE TABLE project (
	title VARCHAR(120) NOT NULL,
	amount NUMERIC(9,2) NOT NULL,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	summary VARCHAR (1000) NOT NULL,
	executive_id SMALLINT NOT NULL,
	program_id SMALLINT NOT NULL,
	supervisor_id SMALLINT NOT NULL,
	grader_id SMALLINT NOT NULL,
	grade TINYINT UNSIGNED NOT NULL,
	grade_date DATE NOT NULL,
	organisation_name VARCHAR(80) NOT NULL,  
	PRIMARY KEY (title),
	CONSTRAINT fk_executive_id 
		FOREIGN KEY (executive_id)
		REFERENCES executive (executive_id) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT fk_program_id 
		FOREIGN KEY (program_id)
		REFERENCES program (program_id) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT fk_supervisor_id 
		FOREIGN KEY (supervisor_id)
		REFERENCES researcher (researcher_id) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT fk_grader_id 
		FOREIGN KEY (grader_id)
		REFERENCES researcher (researcher_id) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT fkey_organisation_name 
		FOREIGN KEY (organisation_name)
		REFERENCES organisation (org_name) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CHECK (grade <= 10),
	CHECK (grade_date < start_date),
	CHECK (DATEDIFF(end_date, start_date) >= 365
			AND DATEDIFF(end_date, start_date) <= 1461),
	CHECK (amount >= 100000.00 
			AND amount <= 1000000.00)
);

CREATE TABLE deliverable (
	project_title VARCHAR(120) NOT NULL,
	deliverable_title VARCHAR(70) NOT NULL,
	summary VARCHAR (1000) NOT NULL,
	deliver_date DATE NOT NULL,
	PRIMARY KEY (project_title, deliverable_title),
	CONSTRAINT fk_project_title 
		FOREIGN KEY (project_title)
		REFERENCES project (title) 
		ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE refers_to (
	project_title VARCHAR(120) NOT NULL,
	field_name VARCHAR(30) NOT NULL,
	PRIMARY KEY (project_title, field_name),
	CONSTRAINT fk_project_title_refer 
		FOREIGN KEY (project_title)
		REFERENCES project (title) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT fk_field_name 
		FOREIGN KEY (field_name)
		REFERENCES scientific_field (name) 
		ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE works_on (
	project_title VARCHAR(120) NOT NULL,
	researcher_id SMALLINT NOT NULL,
	PRIMARY KEY (project_title, researcher_id),
	CONSTRAINT fk_project_title_work 
		FOREIGN KEY (project_title)
		REFERENCES project (title) 
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT fkey_researcher_id 
		FOREIGN KEY (researcher_id)
		REFERENCES researcher (researcher_id) 
		ON DELETE RESTRICT ON UPDATE CASCADE
);















