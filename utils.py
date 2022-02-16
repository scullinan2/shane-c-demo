
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the db connection
def create_db_session():
    engine_str = 'postgresql://{}:{}@{}:{}/{}'.format(environ['DB_USER'], environ['DB_PASS'], environ['DB_HOST'], int(environ['DB_PORT']), environ['DB_NAME'])
    engine     = create_engine(engine_str)
    Session    = sessionmaker(bind=engine, expire_on_commit=False)
    return Session()


def check_records(db, model):
    models = db.query(model).all()
    return True if models else False
