from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, TextField, SubmitField, SelectField, FieldList, BooleanField, DateTimeField
from wtforms.validators import Email, URL
from wtforms.fields.html5 import DateTimeLocalField


class GeneralSearchBar(FlaskForm):
    """Contact form."""
    query_all = StringField('Search All')

class OrganizationForm(FlaskForm):
    """Contact form."""
    org_id = IntegerField('Organization ID')
    url = StringField('URL',[
    	URL(message=("Invalid URL format."))])
    external_id = StringField('Organization External ID')
    name = StringField('Name')
    domain_names = TextField('Organization Domain Names')
    created_at = DateTimeField('Organization Creation Date', format='%Y-%m-%dT%H:%M:%S')
    details = TextField('Organization Details contains')
    shared_tickets = SelectField(
        choices=[(True, 'True'), (False, 'False'), ('','')],
        coerce=lambda x: x == 'True', default=None
    )
    tags = TextField('Organization Tags')


class UserForm(FlaskForm):
    """Contact form."""
    user_id = IntegerField('User ID')
    url = StringField('URL',[
    	URL(message=("Invalid URL format."))])
    external_id = StringField('User External ID')
    name = StringField('Name')
    alias = StringField('Alias')
    created_at = DateTimeLocalField('User Creation Date', format='%Y-%m-%d')
    active = SelectField(
        choices=[(True, 'True'), (False, 'False'), ('','')],
        coerce=lambda x: x == 'True'
    )
    verified = SelectField(
        choices=[(True, 'True'), (False, 'False'), ('','')],
        coerce=lambda x: x == 'True'
    )
    shared = SelectField(
        choices=[(True, 'True'), (False, 'False'), ('','')],
        coerce=lambda x: x == 'True'
    )
    locale = StringField('Locale')
    timezone = StringField('Time Zone')
    last_login_at = DateTimeLocalField('Last user login', format='%Y-%m-%d')
    email = StringField('Email', [
        Email(message=('Not a valid email address.'))])
    phone = StringField('Phone')
    signature = StringField('Signature')
    organization_id = IntegerField('Orangization ID')
    suspended = SelectField(
        choices=[(True, 'True'), (False, 'False'), ('','')],
        coerce=lambda x: x == 'True'
    )
    role = StringField('Role')
    tags = TextField('User Tags', default='{}')


class TicketForm(FlaskForm):
    """Contact form."""
    ticket_id = StringField('Ticket ID')
    url = StringField('URL',[
    	URL(message=("Invalid URL format."))])
    external_id = StringField('Ticket External ID')
    created_at = DateTimeLocalField('Ticket Creation Date', format='%Y-%m-%d')
    type_ = StringField('Ticket Type')
    subject = StringField('Subject')
    description = TextField('Description')
    priority = StringField('Priority')
    status = StringField('Status')
    submitter_id = IntegerField('Submitter ID')
    assignee_id = IntegerField('Assignee ID')
    organization_id = IntegerField('Organization ID')
    tags = TextField('Ticket Tags')
    has_incidents = SelectField(
        choices=[(True, 'True'), (False, 'False'), ('','')],
        coerce=lambda x: x == 'True'
    )
    due_at = DateTimeLocalField('Ticket Due Date', format='%Y-%m-%d')
    via = StringField('Via')
