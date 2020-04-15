import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


engine = create_engine(os.environ['DATABASE_URL'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

if not database_exists(engine.url):
    create_database(engine.url)


def init_db():
    import rt_zen_search.models
    Base.metadata.create_all(bind=engine)