from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import inspect

Base = declarative_base()


class Time(Base):
    __tablename__ = "Time"

    id = Column(Integer, primary_key=True)
    course_id = Column(String(), nullable=False)
    course_name = Column(String(), nullable=False)
    time = Column(String(), nullable=False)

    def __init__(self, course_id, course_name, time):
        self.course_id = course_id
        self.course_name = course_name
        self.time = time

    def __repr__(self):
        return f"{{'course_id': '{self.course_id}', 'course_name': {self.course_name}', 'time': '{self.time}'}}>"


def create_time_table(db):
    inspector = inspect(db.engine)
    if not inspector.has_table("Time"):
        Time.__table__.create(db.engine)


def drop_time_table(db):
    inspector = inspect(db.engine)
    if inspector.has_table("Time"):
        Time.__table__.drop(db.engine)


def add_time(db, course_id, course_name, time):
    new_time = Time(course_id, course_name, time)
    db.session.add(new_time)
    db.session.commit()


def find_time_byname(db, name):
    time = db.session.query(Time).filter_by(course_name=name).all()
    return time


def find_time_byid(db, id):
    time = db.session.query(Time).filter_by(course_id=id).all()
    return time
