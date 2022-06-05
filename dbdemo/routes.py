from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, NoneOf
from dbdemo import app, db ## initially created by __init__.py, need to be used here
from dbdemo.forms import StudentForm, ResearcherForm, Scientific_fieldForm, ProgramForm, ExecutiveForm, OrganisationForm, CompanyForm, UniversityForm, ProjectForm, Research_centreForm, Query3Form

@app.route("/")
def index():
    return render_template("landing.html", pageTitle = "Αρχική σελίδα")

#----------------------------------------------------------------------------------------  View  --------------------------------------------------------------------------------------------------#
@app.route("/view")
def view():
    return render_template("view.html", pageTitle = "Επισκόπηση")

@app.route("/view/scientific_field") #-----------------------------------------------------------------  scientific_field  ------------------------------------------------------------------------#
def viewScientific_field():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM scientific_field")  # students
        column_names = [i[0] for i in cur.description]
        scientific_fields = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_scientific_field.html", scientific_fields = scientific_fields, pageTitle = "Επιστημονικά Πεδία")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/view/program") #---------------------------------------------------------------------------------  program  --------------------------------------------------------------------------#
def viewProgram():
    try:
        form = ProgramForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM program")  # students
        column_names = [i[0] for i in cur.description]
        programs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_program.html", programs = programs, pageTitle = "Πρόγραμμα ΕΛ.ΙΔ.Ε.Κ.", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/view/executive") #--------------------------------------------------------------------------  executive  --------------------------------------------------------------------------#
def viewExecutive():
    try:
        form = ExecutiveForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM executive")  # students
        column_names = [i[0] for i in cur.description]
        executives = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_executive.html", executives = executives, pageTitle = "Στέλεχος ΕΛ.ΙΔ.Ε.Κ.", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/view/organisation") #--------------------------------------------------------------------------  organisation  --------------------------------------------------------------------------#
def viewOrganisation():
    return render_template("view_organisation.html", pageTitle = "Οργανισμοί")

@app.route("/view/organisation/company") #--------------------------------------------------------------------------  company  --------------------------------------------------------------------------#
def viewCompany():
    try:
        CompanyForm.telephone1 = StringField()
        form = CompanyForm()
        cur = db.connection.cursor()
        cur.execute("SELECT c.name, o.abbreviation, o.street, o.street_number, o.postal_code, o.city, c.name_and_abbr, c. address, c.equity FROM organisation o INNER JOIN company_view c ON o.org_name = c.name;")
        column_names = [i[0] for i in cur.description]
        companies = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_company.html", companies = companies, pageTitle = "Εταιρείες", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/view/organisation/university") #--------------------------------------------------------------------------  university  --------------------------------------------------------------------------#
def viewUniversity():
    try:       
        UniversityForm.telephone1 = StringField()
        form = UniversityForm()
        cur = db.connection.cursor()
        cur.execute("SELECT c.name, o.abbreviation, o.street, o.street_number, o.postal_code, o.city, c.name_and_abbr, c. address, c.budget FROM organisation o INNER JOIN university_view c ON o.org_name = c.name;")
        column_names = [i[0] for i in cur.description]
        universities = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_university.html", universities = universities, pageTitle = "Πανεπιστήμια", form = form)
    except Exception as e:
        err = str(e)
        if err == "(4025, 'CONSTRAINT `CONSTRAINT_1` failed for `project_try`.`telephone`')":
            err = 'Τα τηλέφωνα πρέπει να αποτελούνται από 10 δεκαδικά ψηφία.'
        if err == "(4025, 'CONSTRAINT `CONSTRAINT_2` failed for `project_try`.`organisation`')":
            err = "Ο ταχυδρομικός κώδικας πρέπει να αποτελείται από 5 δεκαδικά ψηφία."
        ## if the connection to the database fails, return HTTP response 500
        flash(err, "danger")
        abort(500)

@app.route("/view/organisation/research_centre") #---------------------------------------------------------------  research_centre  --------------------------------------------------------------------------#
def viewResearch_centre():
    try:
        Research_centreForm.telephone1 = StringField()
        form = Research_centreForm()
        cur = db.connection.cursor()
        cur.execute("SELECT c.name, o.abbreviation, o.street, o.street_number, o.postal_code, o.city, c.name_and_abbr, c. address, c.budget_me, c.budget_pa FROM organisation o INNER JOIN research_centre_view c ON o.org_name = c.name;")
        column_names = [i[0] for i in cur.description]
        research_centres = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_research_centre.html", research_centres = research_centres, pageTitle = "Ερευνητικά κέντρα", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/view/researcher") #------------------------------------------------------------------------  researcher  ----------------------------------------------------------------------------#
def viewResearcher():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT org_name FROM organisation")
        column_names = [i[0] for i in cur.description]
        organisations = [dict(zip(column_names, entry))['org_name'] for entry in cur.fetchall()]
        cur.close()
    except Exception as e: ## OperationalError
        flash(str(e), "danger")
    
    ResearcherForm.organisation = SelectField(u'Οργανισμός', choices = organisations, validators = [DataRequired(message = "Υποχρεωτιικό πεδίο.")])
    form = ResearcherForm()
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM researcher")  # students
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_researcher.html", researchers = researchers, pageTitle = "Ερευνητές", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/view/project") #------------------------------------------------------------------------  project  ----------------------------------------------------------------------------#
def viewProject():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT org_name FROM organisation")
        column_names = [i[0] for i in cur.description]
        organisations = [dict(zip(column_names, entry))['org_name'] for entry in cur.fetchall()]
        cur.execute("SELECT executive_id, concat(first_name, ' ', last_name) fullname FROM executive")
        column_names = [i[0] for i in cur.description]
        executives = [dict(zip(column_names, entry))['executive_id'] for entry in cur.fetchall()]
        cur.close()
    except Exception as e: ## OperationalError
        flash(str(e), "danger")
    
    ProjectForm.organisation = SelectField(u'Οργανισμός', choices = organisations, validators = [DataRequired(message = "Υποχρεωτιικό πεδίο.")])
    ProjectForm.executive = SelectField(u'Στέλεχος', choices = executives, validators = [DataRequired(message = "Υποχρεωτιικό πεδίο.")])
    form = ProjectForm()
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT title, amount, start_date, end_date, organisation_name FROM project")  # students
        column_names = [i[0] for i in cur.description]
        projects = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_project.html", projects = projects, pageTitle = "Έργα", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

#----------------------------------------------------------------------------------------  Create  -------------------------------------------------------------------------------------------------#
@app.route("/create")
def create():
    return render_template("create.html", pageTitle = "Δημιουργία")

@app.route("/create/scientific_field", methods = ["GET", "POST"]) #-------------------------------------------  scientific_field  ------------------------------------------------------------------#
def createScientific_field():
    form = Scientific_fieldForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newScientific_field = form.__dict__
        query = "INSERT INTO scientific_field VALUES ('{}');".format(newScientific_field['name'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash(("Το επιστημονικό πεδίο ") + newScientific_field['name'].data + " καταχωρήθηκε επιτυχώς.", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_scientific_field.html", pageTitle = "Δημιουργία επιστημονικού πεδίου", form = form)

@app.route("/create/program", methods = ["GET", "POST"]) #----------------------------------------------  program  ---------------------------------------------------------------------#
def createProgram():
    form = ProgramForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newProgram = form.__dict__
        query = "INSERT INTO program(name, front_office) VALUES ('{}','{}');".format(newProgram['name'].data, newProgram['front_office'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash(("Το πρόγραμμα ") + newProgram['name'].data + " καταχωρήθηκε επιτυχώς.", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_program.html", pageTitle = "Δημιουργία προγράμματος ΕΛ.ΙΔ.Ε.Κ.", form = form)

@app.route("/create/executive", methods = ["GET", "POST"]) #-------------------------------------------------  executive  ---------------------------------------------------------------------#
def createExecutive():
    form = ExecutiveForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newExecutive = form.__dict__
        query = "INSERT INTO executive(first_name, last_name) VALUES ('{}','{}');".format(newExecutive['name'].data, newExecutive['surname'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash(("Το στέλεχος ") + newExecutive['name'].data + " " + newExecutive['surname'].data + " καταχωρήθηκε επιτυχώς.", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_executive.html", pageTitle = "Δημιουργία στελέχους ΕΛ.ΙΔ.Ε.Κ.", form = form)

@app.route("/create/org", methods = ["GET", "POST"]) #----------------------------------------------------------  organisation  ---------------------------------------------------------------------------------#
def createOrganisation():
    return render_template("create_organisation.html", pageTitle = "Δημιουργία οργανισμού")

@app.route("/create/organisation/university", methods = ["GET", "POST"]) #-------------------------------------------------  university  ---------------------------------------------------------------------#
def createUniversity():
    form = UniversityForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newUniversity = form.__dict__
        query1 = "INSERT INTO organisation VALUES ('{}','{}','{}','{}',{},'{}','{}');".format(newUniversity['name'].data, newUniversity['abbreviation'].data, newUniversity['postal_code'].data, newUniversity['street'].data, newUniversity['street_number'].data, newUniversity['city'].data, 'university')
        query2 = "INSERT INTO company VALUES ('{}',{});".format(newUniversity['name'].data, newUniversity['budget'].data)
        queries = [query1, query2, "INSERT INTO telephone VALUES ('{}','{}');".format(newUniversity['telephone1'].data, newUniversity['name'].data)]
        if len(newUniversity['telephone2'].data) > 0:
            queries.append("INSERT INTO telephone VALUES ('{}','{}');".format(newUniversity['telephone2'].data, newUniversity['name'].data))
        if len(newUniversity['telephone3'].data) > 0:
            queries.append("INSERT INTO telephone VALUES ('{}','{}');".format(newUniversity['telephone3'].data, newUniversity['name'].data))
        try:
            cur = db.connection.cursor()
            for query in queries:
                cur.execute(query)
            db.connection.commit()
            cur.close()
            flash(("Το πανεπιστήμιο ") + newUniversity['name'].data + " καταχωρήθηκε επιτυχώς.", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            err = str(e)
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_1` failed for `project_try`.`telephone`')":
                err = 'Τα τηλέφωνα πρέπει να αποτελούνται από 10 δεκαδικά ψηφία.'
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_2` failed for `project_try`.`organisation`')":
                err = "Ο ταχυδρομικός κώδικας πρέπει να αποτελείται από 5 δεκαδικά ψηφία."
            ## if the connection to the database fails, return HTTP response 500
            flash(err, "danger")

    ## else, response for GET request
    return render_template("create_university.html", pageTitle = "Δημιουργία πανεπιστημίου", form = form)

@app.route("/create/organisation/company", methods = ["GET", "POST"]) #-------------------------------------------------  company  ---------------------------------------------------------------------#
def createCompany():
    form = CompanyForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newCompany = form.__dict__
        query1 = "INSERT INTO organisation VALUES ('{}','{}','{}','{}',{},'{}','{}');".format(newCompany['name'].data, newCompany['abbreviation'].data, newCompany['postal_code'].data, newCompany['street'].data, newCompany['street_number'].data, newCompany['city'].data, 'company')
        query2 = "INSERT INTO company VALUES ('{}',{});".format(newCompany['name'].data, newCompany['equity'].data)
        queries = [query1, query2, "INSERT INTO telephone VALUES ('{}','{}');".format(newCompany['telephone1'].data, newCompany['name'].data)]
        if len(newCompany['telephone2'].data) > 0:
            queries.append("INSERT INTO telephone VALUES ('{}','{}');".format(newCompany['telephone2'].data, newCompany['name'].data))
        if len(newCompany['telephone3'].data) > 0:
            queries.append("INSERT INTO telephone VALUES ('{}','{}');".format(newCompany['telephone3'].data, newCompany['name'].data))
        try:
            cur = db.connection.cursor()
            for query in queries:
                cur.execute(query)
            db.connection.commit()
            cur.close()
            flash(("Η εταιρεία ") + newCompany['name'].data + " καταχωρήθηκε επιτυχώς.", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            err = str(e)
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_1` failed for `project_try`.`telephone`')":
                err = 'Τα τηλέφωνα πρέπει να αποτελούνται από 10 δεκαδικά ψηφία.'
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_2` failed for `project_try`.`organisation`')":
                err = "Ο ταχυδρομικός κώδικας πρέπει να αποτελείται από 5 δεκαδικά ψηφία."
            ## if the connection to the database fails, return HTTP response 500
            flash(err, "danger")

    ## else, response for GET request
    return render_template("create_company.html", pageTitle = "Δημιουργία εταιρείας", form = form)

@app.route("/create/organisation/research_centre", methods = ["GET", "POST"]) #-------------------------------------------------  university  ---------------------------------------------------------------------#
def createResearch_centre():
    form = Research_centreForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newResearch_centre = form.__dict__
        query1 = "INSERT INTO organisation VALUES ('{}','{}','{}','{}',{},'{}','{}');".format(newResearch_centre['name'].data, newResearch_centre['abbreviation'].data, newResearch_centre['postal_code'].data, newResearch_centre['street'].data, newResearch_centre['street_number'].data, newResearch_centre['city'].data, 'research_centre')
        query2 = "INSERT INTO research_centre VALUES ('{}',{}, {});".format(newResearch_centre['name'].data, newResearch_centre['budget_me'].data, newResearch_centre['budget_pa'].data)
        queries = [query1, query2, "INSERT INTO telephone VALUES ('{}','{}');".format(newResearch_centre['telephone1'].data, newResearch_centre['name'].data)]
        if len(newResearch_centre['telephone2'].data) > 0:
            queries.append("INSERT INTO telephone VALUES ('{}','{}');".format(newResearch_centre['telephone2'].data, newResearch_centre['name'].data))
        if len(newResearch_centre['telephone3'].data) > 0:
            queries.append("INSERT INTO telephone VALUES ('{}','{}');".format(newResearch_centre['telephone3'].data, newResearch_centre['name'].data))
        try:
            cur = db.connection.cursor()
            for query in queries:
                cur.execute(query)
            db.connection.commit()
            cur.close()
            flash(("Το ερευνητικό κέντρο ") + newResearch_centre['name'].data + " καταχωρήθηκε επιτυχώς.", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            err = str(e)
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_1` failed for `project_try`.`telephone`')":
                err = 'Τα τηλέφωνα πρέπει να αποτελούνται από 10 δεκαδικά ψηφία.'
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_2` failed for `project_try`.`organisation`')":
                err = "Ο ταχυδρομικός κώδικας πρέπει να αποτελείται από 5 δεκαδικά ψηφία."
            ## if the connection to the database fails, return HTTP response 500
            flash(err, "danger")

    ## else, response for GET request
    return render_template("create_research_centre.html", pageTitle = "Δημιουργία ερευνητικού κέντρου", form = form)

@app.route("/create/researcher", methods = ["GET", "POST"]) #-------------------------------------------------------  researcher  ------------------------------------------------------------------#
def createResearcher():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT org_name FROM organisation")
        column_names = [i[0] for i in cur.description]
        organisations = [dict(zip(column_names, entry))['org_name'] for entry in cur.fetchall()]
        organisations.insert(0, "(επιλέξτε ένα από τα παρακάτω)")
        cur.close()
    except Exception as e: ## OperationalError
        flash(str(e), "danger")
    
    ResearcherForm.organisation = SelectField(u'Οργανισμός', choices = organisations, validators = [DataRequired(message = "Υποχρεωτιικό πεδίο."), NoneOf(values = ["(επιλέξτε ένα από τα παρακάτω)"], message = "Υποχρεωτιικό πεδίο.")])
    form = ResearcherForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newResearcher = form.__dict__
        query = "INSERT INTO researcher(first_name, last_name, sex, birth_date, employment_date, organisation_name) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(newResearcher['name'].data, newResearcher['surname'].data, newResearcher['sex'].data, newResearcher['birth_date'].data, newResearcher['employment_date'].data, newResearcher['organisation'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash(("Η ερευνήτρια " if newResearcher['sex'].data == 'f' else "Ο ερευνητής ") + newResearcher['name'].data + " " + newResearcher['surname'].data + " καταχωρήθηκε επιτυχώς.", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_researcher.html", pageTitle = "Δημιουργία ερευνητή", form = form)

@app.route("/create/project", methods = ["GET", "POST"]) #-------------------------------------------------------  project  ------------------------------------------------------------------#
def createProjectr():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT org_name FROM organisation")
        column_names = [i[0] for i in cur.description]
        organisations = [dict(zip(column_names, entry))['org_name'] for entry in cur.fetchall()]
        cur.execute("SELECT executive_id, CONCAT(first_name,' ',last_name) fullname FROM executive")
        column_names = [i[0] for i in cur.description]
        executives_dir = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("SELECT researcher_id, CONCAT(first_name,' ',last_name) fullname FROM researcher")
        column_names = [i[0] for i in cur.description]
        researchers_dir = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("SELECT program_id, name FROM program")
        column_names = [i[0] for i in cur.description]
        programs_dir = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        organisations.insert(0, "(επιλέξτε ένα από τα παρακάτω)")
        cur.close()
    except Exception as e: ## OperationalError
        flash(str(e), "danger")

    executives = [('0', "(επιλέξτε ένα από τα παρακάτω)")]
    researchers = [('0', "(επιλέξτε ένα από τα παρακάτω)")]
    programs = [('0', "(επιλέξτε ένα από τα παρακάτω)")]
    for ex in executives_dir:
        executives.append((str(ex['executive_id']), ex['fullname']))
    for res in researchers_dir:
        researchers.append((str(res['researcher_id']), res['fullname']))
    for p in programs_dir:
        programs.append((str(p['program_id']), p['name']))      
    
    ProjectForm.executive_id = SelectField(u'Στέλεχος ΕΛ.ΙΔ.Ε.Κ.', choices = executives, validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), NoneOf(values = ['0'], message = "Υποχρεωτικό πεδίο.")])
    ProjectForm.supervisor_id = SelectField(u'Υπεύθυνος', choices = researchers, validators = [NoneOf(values = ['0'], message = "Υποχρεωτικό πεδίο.")])
    ProjectForm.grader_id = SelectField(u'Αξιολογητής', choices = researchers, validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), NoneOf(values = ['0'], message = "Υποχρεωτικό πεδίο.")])
    ProjectForm.program_id = SelectField(u'Πρόγραμμα', choices = programs, validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), NoneOf(values = ['0'], message = "Υποχρεωτικό πεδίο.")])    
    ProjectForm.organisation_name = SelectField(u'Οργανισμός', choices = organisations, validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), NoneOf(values = ["(επιλέξτε ένα από τα παρακάτω)"], message = "Υποχρεωτικό πεδίο.")])
    form = ProjectForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newProject = form.__dict__
        query = "INSERT INTO project VALUES ('{}', {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, '{}', '{}');".format(newProject['title'].data, newProject['amount'].data, newProject['start_date'].data, newProject['end_date'].data, newProject['summary'].data, newProject['executive_id'].data, newProject['program_id'].data, newProject['supervisor_id'].data, newProject['grader_id'].data, newProject['grade'].data, newProject['grade_date'].data, newProject['organisation_name'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Το έργο " + newProject['title'].data + " καταχωρήθηκε επιτυχώς.", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_project.html", pageTitle = "Δημιουργία έργου", form = form)

#----------------------------------------------------------------------------------------  Update  --------------------------------------------------------------------------------------------------#

@app.route("/view/program/update/<int:programID>", methods = ["POST"]) #-----------------------------------------------------  program  -------------------------------------------------------------#
def updateProgram(programID):
    form = ProgramForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE program SET name = '{}', front_office = '{}' WHERE program_id = {};".format(updateData['name'].data, updateData['front_office'].data, programID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Το πρόγραμμα ενημερώθηκε επιτυχώς", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("viewProgram"))

@app.route("/view/executive/update/<int:executiveID>", methods = ["POST"]) #---------------------------------------------------  executive  -------------------------------------------------------------#
def updateExecutive(executiveID):
    form = ExecutiveForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE executive SET first_name = '{}', last_name = '{}' WHERE executive_id = {};".format(updateData['name'].data, updateData['surname'].data, executiveID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Το στέλεχος ενημερώθηκε επιτυχώς", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("viewExecutive"))

@app.route("/view/organisation/university/update/<string:name>", methods = ["POST"]) #---------------------------------------------------  university  -------------------------------------------------------------#
def updateUniversity(name):
    form = UniversityForm()
    form.name = StringField()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query1 = "UPDATE university SET budget = {} WHERE name = '{}';".format(updateData['budget'].data, name)
        query2 = "UPDATE organisation SET abbreviation = '{}', street = '{}', street_number = '{}', postal_code = '{}', city = '{}' WHERE org_name = '{}';".format(updateData['abbreviation'].data, updateData['street'].data, updateData['street_number'].data,updateData['postal_code'].data, updateData['city'].data, name)
        try:
            cur = db.connection.cursor()
            cur.execute(query1)
            cur.execute(query2)
            db.connection.commit()
            cur.close()
            flash("Το πανεπιστήμιο ενημερώθηκε επιτυχώς", "success")
        except Exception as e:
            err = str(e)
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_1` failed for `project_try`.`telephone`')":
                err = 'Τα τηλέφωνα πρέπει να αποτελούνται από 10 δεκαδικά ψηφία.'
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_2` failed for `project_try`.`organisation`')":
                err = "Ο ταχυδρομικός κώδικας πρέπει να αποτελείται από 5 δεκαδικά ψηφία."
            ## if the connection to the database fails, return HTTP response 500
            flash(err, "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("viewUniversity"))

@app.route("/view/organisation/company/update/<string:name>", methods = ["POST"]) #---------------------------------------------------  company  -------------------------------------------------------------#
def updateCompany(name):
    form = CompanyForm()
    form.name = StringField()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query1 = "UPDATE company SET equity = {} WHERE name = '{}';".format(updateData['equity'].data, name)
        query2 = "UPDATE organisation SET abbreviation = '{}', street = '{}', street_number = '{}', postal_code = '{}', city = '{}' WHERE org_name = '{}';".format(updateData['abbreviation'].data, updateData['street'].data, updateData['street_number'].data,updateData['postal_code'].data, updateData['city'].data, name)
        try:
            cur = db.connection.cursor()
            cur.execute(query1)
            cur.execute(query2)
            db.connection.commit()
            cur.close()
            flash("Η εταιρεία ενημερώθηκε επιτυχώς", "success")
        except Exception as e:
            err = str(e)
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_1` failed for `project_try`.`telephone`')":
                err = 'Τα τηλέφωνα πρέπει να αποτελούνται από 10 δεκαδικά ψηφία.'
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_2` failed for `project_try`.`organisation`')":
                err = "Ο ταχυδρομικός κώδικας πρέπει να αποτελείται από 5 δεκαδικά ψηφία."
            ## if the connection to the database fails, return HTTP response 500
            flash(err, "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("viewCompany"))

@app.route("/view/organisation/research_centre/update/<string:name>", methods = ["POST"]) #---------------------------------------  research_centre  -------------------------------------------------------#
def updateResearch_centre(name):
    form = Research_centreForm()
    form.name = StringField()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query1 = "UPDATE research_centre SET budget_me = {}, budget_pa = {} WHERE name = '{}';".format(updateData['budget_me'].data, updateData['budget_pa'].data, name)
        query2 = "UPDATE organisation SET abbreviation = '{}', street = '{}', street_number = '{}', postal_code = '{}', city = '{}' WHERE org_name = '{}';".format(updateData['abbreviation'].data, updateData['street'].data, updateData['street_number'].data,updateData['postal_code'].data, updateData['city'].data, name)
        try:
            cur = db.connection.cursor()
            cur.execute(query1)
            cur.execute(query2)
            db.connection.commit()
            cur.close()
            flash("Το ερευνητικό κέντρο ενημερώθηκε επιτυχώς", "success")
        except Exception as e:
            err = str(e)
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_1` failed for `project_try`.`telephone`')":
                err = 'Τα τηλέφωνα πρέπει να αποτελούνται από 10 δεκαδικά ψηφία.'
            if err == "(4025, 'CONSTRAINT `CONSTRAINT_2` failed for `project_try`.`organisation`')":
                err = "Ο ταχυδρομικός κώδικας πρέπει να αποτελείται από 5 δεκαδικά ψηφία."
            ## if the connection to the database fails, return HTTP response 500
            flash(err, "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("viewResearch_centre"))

@app.route("/view/researcher/update/<int:researcherID>", methods = ["POST"]) #----------------------------------------------  researcher  -------------------------------------------------------------#
def updateResearcher(researcherID):
    form = ResearcherForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE researcher SET first_name = '{}', last_name = '{}', sex = '{}', birth_date = '{}', employment_date = '{}', organisation_name = '{}' WHERE researcher_id = \'{}\';".format(updateData['name'].data, updateData['surname'].data, updateData['sex'].data, updateData['birth_date'].data, updateData['employment_date'].data, updateData['organisation'].data, researcherID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Ο ερευνητής ενημερώθηκε επιτυχώς", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("viewResearcher"))

#----------------------------------------------------------------------------------------  Delete  --------------------------------------------------------------------------------------------------#

@app.route("/view/scientific_field/delete/<string:name>", methods = ["POST"]) #-------------------------------------------  scientific_field  -------------------------------------------------------#
def deleteScientific_field(name):
    query = f"DELETE FROM scientific_field WHERE name = \'{name}\';"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Το επιστημονικό πεδίο διαγράφηκε επιτυχώς", "primary")
    except Exception as e:
        flash("Η διαγραφή απέτυχε.", "danger")
    return redirect(url_for("viewScientific_field"))

@app.route("/view/program/delete/<int:id>", methods = ["POST"]) #---------------------------------------------------------  program  -----------------------------------------------------------------#
def deleteProgram(id):
    query = f"DELETE FROM program WHERE program_id = {id};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Το πρόγραμμα διαγράφηκε επιτυχώς", "primary")
    except Exception as e:
        flash("Η διαγραφή απέτυχε.", "danger")
    return redirect(url_for("viewProgram"))

@app.route("/view/executive/delete/<int:id>", methods = ["POST"]) #---------------------------------------------------------  executive  -----------------------------------------------------------------#
def deleteExecutive(id):
    query = f"DELETE FROM executive WHERE executive_id = {id};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Το στέλεχος διαγράφηκε επιτυχώς", "primary")
    except Exception as e:
        flash("Η διαγραφή απέτυχε.", "danger")
    return redirect(url_for("viewExecutive"))

@app.route("/view/organisation/university/delete/<string:name>", methods = ["POST"]) #---------------------------------------------------------  university  -----------------------------------------------------------------#
def deleteUniversity(name):
    query1 = f"DELETE FROM university WHERE name = '{name}';"
    query2 = f"DELETE FROM telephone WHERE organisation_name = '{name}';"
    query3 = f"DELETE FROM organisation WHERE org_name = '{name}';"
    try:
        cur = db.connection.cursor()
        cur.execute(query1)
        cur.execute(query2)
        cur.execute(query3)
        db.connection.commit()
        cur.close()
        flash("Το πανεπιστήμιο διαγράφηκε επιτυχώς", "primary")
    except Exception as e:
        flash("Η διαγραφή απέτυχε.", "danger")
    return redirect(url_for("viewUniversity"))

@app.route("/view/organisation/company/delete/<string:name>", methods = ["POST"]) #---------------------------------------------------------  company  -----------------------------------------------------------------#
def deleteCompany(name):
    query1 = f"DELETE FROM company WHERE name = '{name}';"
    query2 = f"DELETE FROM telephone WHERE organisation_name = '{name}';"
    query3 = f"DELETE FROM organisation WHERE org_name = '{name}';"
    try:
        cur = db.connection.cursor()
        cur.execute(query1)
        cur.execute(query2)
        cur.execute(query3)
        db.connection.commit()
        cur.close()
        flash("Η εταιρεία διαγράφηκε επιτυχώς", "primary")
    except Exception as e:
        flash("Η διαγραφή απέτυχε.", "danger")
    return redirect(url_for("viewCompany"))

@app.route("/view/organisation/research_centre/delete/<string:name>", methods = ["POST"]) #---------------------------------------------------------  university  -----------------------------------------------------------------#
def deleteResearch_centre(name):
    query1 = f"DELETE FROM research_centre WHERE name = '{name}';"
    query2 = f"DELETE FROM telephone WHERE organisation_name = '{name}';"
    query3 = f"DELETE FROM organisation WHERE org_name = '{name}';"
    try:
        cur = db.connection.cursor()
        cur.execute(query1)
        cur.execute(query2)
        cur.execute(query3)
        db.connection.commit()
        cur.close()
        flash("Το ερευνηρικό κέντρο διαγράφηκε επιτυχώς", "primary")
    except Exception as e:
        flash("Η διαγραφή απέτυχε.", "danger")
    return redirect(url_for("viewResearch_centre"))

@app.route("/view/researcher/delete/<int:researcherID>", methods = ["POST"]) #------------------------------------------------  researcher  ----------------------------------------------------------#
def deleteResearcher(researcherID):
    query = f"DELETE FROM researcher WHERE researcher_id = {researcherID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Ο/Η ερευντητής/τρια διαγράφηκε επιτυχώς", "primary")
    except Exception as e:
        flash("Η διαγραφή απέτυχε.", "danger")
    return redirect(url_for("viewResearcher"))

@app.route("/view/project/delete/<string:name>", methods = ["POST"]) #---------------------------------------------------------  university  -----------------------------------------------------------------#
def deleteProject(name):
    query1 = f"DELETE FROM refers_to WHERE project_title = '{name}';"
    query2 = f"DELETE FROM works_on WHERE project_title = '{name}';"
    query3 = f"DELETE FROM project WHERE title = '{name}';"
    try:
        cur = db.connection.cursor()
        cur.execute(query1)
        cur.execute(query2)
        cur.execute(query3)
        db.connection.commit()
        cur.close()
        flash("Το έργο διαγράφηκε επιτυχώς", "primary")
    except Exception as e:
        flash("Η διαγραφή απέτυχε.", "danger")
    return redirect(url_for("viewProject"))

#----------------------------------------------------------------------------------------  Questions  -----------------------------------------------------------------------------------------------#
@app.route("/questions")
def Questions():
    return render_template("questions.html", pageTitle = "Συχνές ερωτήσεις")

@app.route("/questions/2")
def Questions2():
    return render_template("questions_2.html", pageTitle = "Όψεις του σχεσιακού μοντέλου")

@app.route("/questions/2_1")
def Questions2_1():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT DISTINCT fullname FROM researchers_on_projects;")  # students
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("SELECT fullname, title FROM researchers_on_projects ORDER BY fullname;")  # students
        column_names = [i[0] for i in cur.description]
        proj_per_res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        reslist = []
        for r in researchers:
            reslist.append({'fullname':r['fullname'],'titles':['']})
        for pdict in proj_per_res:
            for i in range (0,len(reslist)):
               if pdict['fullname'] == reslist[i]['fullname']:
                    u = reslist[i]['titles']
                    u .append(pdict['title'])
                    reslist[i]['titles'] = u
        cur.close()
        return render_template("questions_2_1.html", reslist = reslist, pageTitle = "Έργα ανά ερευνητή")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)
    
@app.route("/questions/2_2")
def Questions2_2():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM scientific_field;")  # students
        column_names = [i[0] for i in cur.description]
        fields = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("SELECT field_name field, project_title title FROM refers_to ORDER BY field_name;")  # students
        column_names = [i[0] for i in cur.description]
        proj_per_field = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        reslist = []
        for r in fields:
            reslist.append({'field':r['name'],'titles':['']})
        for pdict in proj_per_field:
            for i in range (0,len(reslist)):
               if pdict['field'] == reslist[i]['field']:
                    u = reslist[i]['titles']
                    u .append(pdict['title'])
                    reslist[i]['titles'] = u
        cur.close()
        return render_template("questions_2_2.html", reslist = reslist, pageTitle = "Έργα ανά επιστημονικό πεδίο")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/questions/3", methods = ["GET", "POST"]) 
def Questions3():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM scientific_field")
        column_names = [i[0] for i in cur.description]
        fields = [dict(zip(column_names, entry))['name'] for entry in cur.fetchall()]
        fields.insert(0, "(επιλέξτε επιστημονικό πεδίο)")
        cur.close()
    except Exception as e: ## OperationalError
        flash(str(e), "danger")
    
    titles = []
    fullnames = []
    Query3Form.field = SelectField(u'Επιστημονικό πεδίο', choices = fields, validators = [DataRequired(message = "Υποχρεωτιικό πεδίο."), NoneOf(values = ["(επιλέξτε επιστημονικό πεδίο)"], message = "Υποχρεωτιικό πεδίο.")])   
    form = Query3Form()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        Field = form.__dict__
        query1 = """ 
            SELECT DISTINCT rp.title
            FROM researchers_on_projects rp INNER JOIN project p
            WHERE rp.title = p.title AND  
            p.title = SOME (SELECT project_title FROM refers_to WHERE field_name='{}')
            AND p.start_date < CURRENT_DATE
            AND DATEDIFF(CURRENT_DATE, p.start_date) < 365 
            AND p.end_date > CURRENT_DATE;
        """.format(Field['field'].data)
        query2 = """ 
            SELECT DISTINCT rp.fullname
            FROM researchers_on_projects rp INNER JOIN project p
            WHERE rp.title = p.title AND  
            p.title = SOME (SELECT project_title FROM refers_to WHERE field_name='{}')
            AND p.start_date < CURRENT_DATE
            AND DATEDIFF(CURRENT_DATE, p.start_date) < 365 
            AND p.end_date > CURRENT_DATE;
        """.format(Field['field'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query1)
            column_names = [i[0] for i in cur.description]
            titles = [dict(zip(column_names, entry))['title'] for entry in cur.fetchall()]
            cur.execute(query2)
            column_names = [i[0] for i in cur.description]
            fullnames = [dict(zip(column_names, entry))['fullname'] for entry in cur.fetchall()]
            db.connection.commit()
            cur.close()
            return render_template("questions_3.html", pageTitle = "Έργα και ερευνητές ανά επιστημονικό πεδίο", form = form, titles = titles, fullnames = fullnames)
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("questions_3.html", pageTitle = "Έργα και ερευνητές ανά επιστημονικό πεδίο", form = form, titles = titles, fullnames = fullnames)

@app.route("/questions/5")
def Questions5():
    try:
        cur = db.connection.cursor()
        query = """ 
            SELECT CONCAT(fp.field1, ' - ', fp.field2) field_pair, COUNT(title) cnt
            FROM (
                SELECT fp1.name field1, fp2.name field2, fp1.title
                FROM (
                    SELECT f1.name, r1.project_title title
                    FROM scientific_field f1 INNER JOIN refers_to r1 ON f1.name = r1.field_name
                ) fp1
                INNER JOIN (
                    SELECT f2.name, r2.project_title title
                    FROM scientific_field f2 INNER JOIN refers_to r2 ON f2.name = r2.field_name
                ) fp2
                ON fp1.title = fp2.title AND fp1.name < fp2.name
            ) fp
            GROUP BY fp.field1, fp.field2
            ORDER BY cnt DESC LIMIT 3;
        """
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("questions_5.html", researchers = researchers, pageTitle = "3 συχνότερα ζεύγη επιστημονικών πεδίων")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/questions/6")
def Questions6():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT fullname, cnt FROM young_help WHERE cnt = (select MAX(cnt) FROM young_help);")
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("questions_6.html", researchers = researchers, pageTitle = "Νέοι ερευνητές με τα περισσότερα ενεργά έργα")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/questions/7")
def Questions7():
    try:
        cur = db.connection.cursor()
        query = """ 
            SELECT fullname, org_name, SUM(amount) esum
            FROM executive_company            
            GROUP BY executive_id, org_name
            ORDER BY esum DESC LIMIT 5;
        """
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        executives = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("questions_7.html", executives = executives, pageTitle = "Top 5 στελέχη ΕΛ.ΙΔ.Ε.Κ. με το μεγαλύτερο ποσό χρηματοδότησης σε μία εταιρεία")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/questions/8")
def Questions8():
    try:
        cur = db.connection.cursor()
        query = """ 
            SELECT nt.fullname, COUNT(nt.title) cnt
            FROM (
                SELECT fullname, title 
                FROM researchers_on_projects
                WHERE title IN ((SELECT title FROM project) EXCEPT (SELECT DISTINCT project_title FROM deliverable))
            ) nt
            GROUP BY nt.fullname
            HAVING COUNT(nt.title) >= 5
            ORDER BY nt.fullname; 
        """
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("questions_8.html", researchers = researchers, pageTitle = "Ερευνητές τουλάχιστον 5 έργων χωρίς παραδοτέα")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

#----------------------------------------------------------------------------------------  Errors  --------------------------------------------------------------------------------------------------#
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500
