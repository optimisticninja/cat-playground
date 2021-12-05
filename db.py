from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String

engine = create_engine("postgresql+psycopg2://root:root@localhost/reversibleca", echo=True)
Base = declarative_base()


class StateTransition(Base):
    __tablename__ = "state"
    epoch = Column(Integer, primary_key=True)
    rule = Column(Integer, primary_key=True)
    neighborhood_sites = Column(Integer, primary_key=True)
    boundary = Column(Integer, primary_key=True)
    biasing = Column(Integer, primary_key=True)
    state = Column(String)

    def __init__(self, epoch, rule, neighborhood_sites, boundary, biasing, state):
        self.epoch = epoch
        self.rule = rule
        self.neighborhood_sites = neighborhood_sites
        self.boundary = boundary
        self.biasing = biasing
        self.state = state


Base.metadata.create_all(engine)