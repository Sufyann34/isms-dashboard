from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base


class System(Base):
    __tablename__ = "systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner = Column(String)


class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    likelihood = Column(Integer)
    impact = Column(Integer)
    system_id = Column(Integer, ForeignKey("systems.id"))


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    severity = Column(String)
    status = Column(String)
    remediation_plan = Column(String)
    system_id = Column(Integer, ForeignKey("systems.id"))