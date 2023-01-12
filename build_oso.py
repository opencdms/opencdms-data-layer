from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from oso import Oso
import os
from sqlalchemy_oso import authorized_sessionmaker, register_models
from data_model import *
from sqlalchemy.orm import sessionmaker, Session, close_all_sessions

oso = Oso()
register_models(oso,Base)
oso.load_files(["policy.polar"])

UID = os.environ["POSTGRES_USER"]
PWD = os.environ["POSTGRES_PASSWORD"]
DBNAME = os.environ["POSTGRES_DB"]

connection_url = f"postgresql+psycopg2://{UID}:{PWD}@opencdms-database:5432/{DBNAME}"
engine = create_engine(connection_url)


def get_authenticated_user(user_id: str):
    SessionLocal = sessionmaker(autocommit=False,class_=Session, autoflush=False, bind=engine)
    session = SessionLocal()
    user = session.query(Users).filter(Users.id == user_id).one()
    return user




AuthorizedSession = authorized_sessionmaker(bind=engine,
                                             get_oso=lambda: oso,
                                             get_user=lambda: get_authenticated_user("1"),
                                             get_checked_permissions=lambda: { Observations: "read" })
manager_session = AuthorizedSession()


user_1_observations = manager_session.query(Observations).all()

