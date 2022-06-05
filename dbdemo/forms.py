from sys import orig_argv
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, DateField, IntegerField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NoneOf

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class StudentForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])

    surname = StringField(label = "Surname", validators = [DataRequired(message = "Surname is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])

    number = StringField(label = "Phone Number", validators = [DataRequired(message = "Phone number is a required field."), Length(10, 10, message = "Phone number must be 10 digits long.")])

    submit = SubmitField("Create")

class Scientific_fieldForm(FlaskForm):
    name = StringField(label = "Όνομα", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 30)])
    submit = SubmitField("Δημιουργία")

front_offices = ['(επιλέξτε ένα από τα παρακάτω)','Ανθρωπιστική Διεύθυνση','Διεύθυνση Θετικών Επιστημών','Αρχαιολογική Διεύθυνση','Περιβαλλοντική Διεύθυνση','Πολιτιστική Διεύθυνση',
'Διεύθυνση Ανάπλασης','Διεύθυνση Δημοτικών Έργων','Διεύθυνση Ενέργειας','Διεύθυνση Υποδομών','Ευρωπαϊκή Διεύθυνση']

class ProgramForm(FlaskForm):
    name = StringField(label = "Όνομα", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 150)])
    front_office = SelectField(u'Διεύθυνση ΕΛ.ΙΔ.Ε.Κ.', choices = front_offices, validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), NoneOf(values = ["(επιλέξτε ένα από τα παρακάτω)"], message = "Υποχρεωτικό πεδίο.")])
    submit = SubmitField("Δημιουργία")

class ExecutiveForm(FlaskForm):
    name = StringField(label = "Όνομα", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 30)])
    surname = StringField(label = "Επώνυμο", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 30)])
    submit = SubmitField("Δημιουργία")

class OrganisationForm(FlaskForm):
    name = StringField(label = "Όνομα", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 80)])
    abbreviation = StringField(label = "Συντομογραφία", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 15)])
    postal_code = StringField(label = "Ταχυδρομικός Κώδικας", validators = [DataRequired(message = "Υποχρεωτικό πεδίο"), Length(5, 5, message = "Ο ταχυδρομικός κώδικας πρέπει να αποτελείται από 5 δεκαδικά ψηφία.")])
    street = StringField(label = "Οδός", validators = [DataRequired(message = "Υποχρεωικό πεδίο."), Length(1, 50)])
    street_number = IntegerField(label = "Αριθμός", validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    city = StringField(label = "Πόλη", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 20)])
    telephone1 = StringField(label = "Τηλέφωνο 1", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(10, 10, message = "Το τηλέφωνο πρέπει να αποτελείται από 10 δεκαδικά ψηφία.")])
    telephone2 = StringField(label = "Τηλέφωνο 2", validators = [Length(0, 10, message = "Το τηλέφωνο πρέπει να αποτελείται από 10 δεκαδικά ψηφία.")])
    telephone3 = StringField(label = "Τηλέφωνο 3", validators = [Length(0, 10, message = "Το τηλέφωνο πρέπει να αποτελείται από 10 δεκαδικά ψηφία.")])
    submit = SubmitField("Δημιουργία")

class CompanyForm(OrganisationForm):
    equity = DecimalField(label = "Ίδια κεφάλαια", places = 2, validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])

class UniversityForm(OrganisationForm):
    budget = DecimalField(label = "Προϋπολογισμός", places = 2, validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])

class Research_centreForm(OrganisationForm):
    budget_me = DecimalField(label = "Προϋπολογισμός Υ.Π.", places = 2, validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    budget_pa = DecimalField(label = "Προϋπολογισμός από ιδιωτικές δράσεις", places = 2, validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])

class ResearcherForm(FlaskForm):        
    name = StringField(label = "Όνομα", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 30)])
    surname = StringField(label = "Επώνυμο", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 30)])
    sex = SelectField(label = "Φύλο", choices = [('f', 'Γυναίκα'), ('m', 'Άνδρας'), ('o', 'Άλλο')], validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    birth_date = DateField(label = "Ημερομηνία Γέννησης", validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    employment_date = DateField(label = "Ημερομηνία Πρόσληψης", validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    submit = SubmitField("Δημιουργία")

class ProjectForm(FlaskForm):
    title = StringField(label = "Τίτλος", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 120)])
    amount = DecimalField(label = "Ποσό επιχορήγησης", places = 2, validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    start_date = DateField(label = "Ημερομηνία Έναρξης", validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    end_date = DateField(label = "Ημερομηνία Λήξης", validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    summary = TextAreaField(label = "Περίληψη", validators = [DataRequired(message = "Υποχρεωτικό πεδίο."), Length(1, 1000)])
    grade = IntegerField(label = "Βαθμός", validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    grade_date = DateField(label = "Ημερομηνία Αξιολόγησης", validators = [DataRequired(message = "Υποχρεωτικό πεδίο.")])
    submit = SubmitField("Δημιουργία")

class Query3Form(FlaskForm):
    submit = SubmitField("Ενημέρωση")

