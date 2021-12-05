from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String

engine = create_engine("postgresql+psycopg2://root:root@localhost/reversibleca", echo=True)
Base = declarative_base()


class StateTransition(Base):
    __tablename__ = "state"
    epoch = Column(Integer, primary_key=True)
    rule = Column(Integer, primary_key=True)
    state = Column(String)

    def __init__(self, epoch, rule, state):
        self.epoch = epoch
        self.rule = rule
        self.state = state


Base.metadata.create_all(engine)