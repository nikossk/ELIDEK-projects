# ELIDEK-projects

## Overview
In this project we build a database to manage the projects funded by an institution called ELIDEK.

## Requirements
- MySQl for Windows
- Python, with the additional libraries :
  - Flask
  - Flask-MySQLdb
  - Flask-WTForms

## ER Diagram
<div align="center">
  <img src="https://github.com/nikossk/ELIDEK-projects/blob/main/images/ER%20diagram.png?raw=true" width="980" height="600"/>
</div>

## Relational Diagram
<div align="center">
  <img src="https://github.com/nikossk/ELIDEK-projects/blob/main/images/Relational%20diagram.png?raw=true" width="700" height="710"/>
</div>

## Installation
1. Firstly, initialize a mysql database at a localhost.
2. Connect in mysql host from a terminal.
3. Run the following sql files strictly at this order:
   - project_try_schema.sql
    - project_create_company_view.sql
    - project_create_researchers_on_projects.sql
   - project_executive_company.sql
   - project_create_young_researchers.sql
   - project_create_young_help.sql
   - project_try_insert_data_sf_exec_prog.sql
   - project_insert_data_organisation.sql
   - project_try_insert_data_telephone.sql
   - project_insert_data_uni_comp_res.sql
    - project_insert_data_researcher.sql
    - project_insert_data_project.sql
    - project_insert_data_deliverable.sql
    - project_isert_data_refers_to.sql
    - project_insert_data_works_on.sql
4. Install all necesary packages for the app by executing the command :
    ```
    pip install -r requirements.txt
    ```
   in your terminal.

5. Restart your computer and run the `run.py` file. 
