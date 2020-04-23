import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(os.environ['DATABASE_URL'], echo=True)
Base = declarative_base()


class Organizations(Base):
    """Define Org base class for SQLAlchemy."""

    __tablename__ = "organizations"
    _id = Column(Integer, primary_key=True)
    url = Column(String)
    external_id = Column(String)
    name = Column(String)
    domain_names = Column(ARRAY(String))
    created_at = Column(String)
    details = Column(String)
    shared_tickets = Column(Boolean)
    tags = Column(ARRAY(String))

    def __repr__(self):
        return "{}".format(self.name)


class Users(Base):
    """Define User base class for SQLAlchemy."""

    __tablename__ = "users"
    _id = Column(Integer, primary_key=True)
    url = Column(String)
    external_id = Column(String)
    name = Column(String)
    alias = Column(String)
    created_at = Column(String)
    active = Column(Boolean)
    verified = Column(Boolean)
    shared = Column(Boolean)
    locale = Column(String)
    timezone = Column(String)
    last_login_at = Column(String)
    email = Column(String)
    phone = Column(String)
    signature = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations._id"))
    tags = Column(ARRAY(String))
    suspended = Column(Boolean)
    role = Column(String)

    def __repr__(self):
        return "{}".format(self.name)


class Tickets(Base):
    """Define Ticket base class for SQLAlchemy."""

    __tablename__ = "tickets"
    _id = Column(String, primary_key=True)
    url = Column(String)
    external_id = Column(String)
    created_at = Column(String)
    type_ = Column(String)
    subject = Column(String)
    description = Column(String)
    priority = Column(String)
    status = Column(String)
    submitter_id = Column(Integer, ForeignKey("users._id"))
    assignee_id = Column(Integer, ForeignKey("users._id"))
    organization_id = Column(Integer, ForeignKey("organizations._id"))
    tags = Column(ARRAY(String))
    has_incidents = Column(Boolean)
    due_at = Column(String)
    via = Column(String)

    def __repr__(self):
        return "{}".format(self.subject)


def create_tables():
    Base.metadata.create_all(engine)
