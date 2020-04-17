from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, TextField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, URL
from wtforms.fields.html5 import DateTimeLocalField


class GeneralSearchBar(FlaskForm):
    """Contact form."""
    search = StringField('search')
    submit = SubmitField('Submit')

class OrganizationForm(FlaskForm):
    """Contact form."""
    org_id = IntegerField('Organization ID')
    url = StringField('URL',[
    	URL(message=("Invalid URL format."))])
    external_id = StringField('Organization External ID')
    name = StringField('Name')
    domain_name = FieldList(StringField('Organization Domain Names'))
    created_at = DateTimeLocalField('Organization Creation Date', format='%m/%d/%y')
    details = TextField('Organization Details contains')
    shared_tickets = BooleanField('Shared Tickets')
    tags = FieldList(StringField('Organization Tags'))
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    """Contact form."""
    user_id = IntegerField('User ID')
    url = StringField('URL',[
    	URL(message=("Invalid URL format."))])
    external_id = StringField('User External ID')
    name = StringField('Name')
    alias = StringField('Alias')
    domain_name = FieldList(StringField('Organization Domain Names'))
    created_at = DateTimeLocalField('Organization Creation Date', format='%m/%d/%y')
    active = BooleanField('Active')
    verified = BooleanField('Verified')
    shared = BooleanField('Shared Tickets')
    locale = StringField('TimeZone')
    last_login_at = DateTimeLocalField('Last user login', format='%m/%d/%y')
    email = StringField('Email', [
        Email(message=('Not a valid email address.'))])
    phone = StringField('Phone')
    signature = StringField('Signature')
    organization_id = IntegerField('Orangization ID')
    tags = FieldList(StringField('Organization Tags'))
    submit = SubmitField('Submit')


class TicketForm(FlaskForm):
    """Contact form."""
    ticket_id = IntegerField('Ticket ID')
    url = StringField('URL',[
    	URL(message=("Invalid URL format."))])
    external_id = StringField('Ticket External ID')
    created_at = DateTimeLocalField('Ticket Creation Date', format='%m/%d/%y')
    ticket_type = StringField('Ticket Type')
    subject = StringField('Subject')
    description = TextField('Description')
    priority = StringField('Priority')
    status = StringField('Status')
    submitter_id = IntegerField('Submitter ID')
    assignee_id = IntegerField('Assignee ID')
    organization_id = IntegerField('Organization ID')
    tags = FieldList(StringField('Ticket Tags'))
    has_incidents = BooleanField('Has Incidents?')
    due_at = DateTimeLocalField('Ticket Due Date', format='%m/%d/%y')
    via = StringField('Via')
    submit = SubmitField('Submit')
