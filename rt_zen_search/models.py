from app import db


class Organizations(db.Model):
    """Define Org table for SQLAlchemy"""
    __tablename__ = "organizations"
    _id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    external_id = db.Column(db.String)
    name = db.Column(db.String)
    domain_names = db.Column(db.ARRAY(db.String))
    created_at = db.Column(db.String)
    details = db.Column(db.String)
    shared_tickets = db.Column(db.Boolean)
    tags = db.Column(db.ARRAY(db.String))

    def __repr__(self):
        return "{}".format(self.name)


class Users(db.Model):
    """Define User table for SQLAlchemy"""
    __tablename__ = "users"
    _id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    external_id = db.Column(db.String)
    name = db.Column(db.String)
    alias = db.Column(db.String)
    created_at = db.Column(db.String)
    active = db.Column(db.Boolean)
    verified = db.Column(db.Boolean)
    shared = db.Column(db.Boolean)
    locale = db.Column(db.String)
    timezone = db.Column(db.String)
    last_login_at = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    signature = db.Column(db.String)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations._id"))
    tags = db.Column(db.ARRAY(db.String))
    suspended = db.Column(db.Boolean)
    role = db.Column(db.String)

    def __repr__(self):
        return "{}".format(self.name)


class Tickets(db.Model):
    """Define Ticket table for SQLAlchemy"""
    __tablename__ = "tickets"
    _id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    external_id = db.Column(db.String)
    created_at = db.Column(db.String)
    tick_type = db.Column(db.String)
    subject = db.Column(db.String)
    description = db.Column(db.String)
    priority = db.Column(db.String)
    status = db.Column(db.String)
    submitter_id = db.Column(db.Integer, db.ForeignKey("users._id"))
    assignee_id = db.Column(db.Integer, db.ForeignKey("users._id"))
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations._id"))
    tags = db.Column(db.ARRAY(db.String))
    has_incedents = db.Column(db.Boolean)
    due_at = db.Column(db.String)
    via = db.Column(db.String)

    def __repr__(self):
        return "{}".format(self.subject)