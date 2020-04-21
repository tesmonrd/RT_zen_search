from flask_table import Table, Col


class OrgTable(Table):
    """Define Org query data for data loading/querying in SQLAlchemy."""
    classes = ['table', 'table-bordered', 'table-striped']
    _id = Col('_id')
    url = Col('url')
    external_id = Col('external_id')
    name = Col('name')
    domain_names = Col('domain_names')
    created_at = Col('created_at')
    details = Col('details')
    shared_tickets = Col('shared_tickets')
    tags = Col('tags')


class UserTable(Table):
    """Define User query data for data loading/querying in SQLAlchemy."""
    classes = ['table', 'table-bordered', 'table-striped']
    _id = Col('_id')
    url = Col('url')
    external_id = Col('external_id')
    name = Col('name')
    alias = Col('alias')
    created_at = Col('created_at')
    active = Col('active')
    verified = Col('verified')
    shared = Col('shared')
    locale = Col('locale')
    timezone = Col('timezone')
    last_login_at = Col('last_login_at')
    email = Col('email')
    phone = Col('phone')
    signature = Col('signature')
    organization_id = Col('organization_id')
    tags = Col('tags')
    suspended = Col('suspended')
    role = Col('role')


class TicketTable(Table):
    """Define Ticket query data for data loading/querying in SQLAlchemy."""
    classes = ['table', 'table-bordered', 'table-striped']
    _id = Col('_id')
    url = Col('url')
    external_id = Col('external_id')
    created_at = Col('name')
    type_ = Col('alias')
    subject = Col('created_at')
    description = Col('active')
    priority = Col('verified')
    status = Col('status')
    submitter_id = Col('submitter_id')
    assignee_id = Col('assignee_id')
    organization_id = Col('organization_id')
    tags = Col('tags')
    has_incidents = Col('has_incidents')
    due_at = Col('due_at')
    via = Col('via')
