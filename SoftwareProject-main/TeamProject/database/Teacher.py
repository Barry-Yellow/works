"""
教师信息
懒得写了，要用的话自己考虑要不要补全吧
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy import inspect

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "Teacher"

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False, unique=True)
    email = Column(String(), nullable=False, unique=True)
    gender = Column(Enum("男", "女", name="gender_enum"), nullable=True)
    major = Column(String(), nullable=False)
    title = Column(String(), nullable=False)

    def __init__(self, name, email, gender, major, title):
        self.name = name
        self.email = email
        self.gender = gender
        self.major = major
        self.title = title

    def __repr__(self):
        return f"<Teacher(name='{self.name}', email='{self.email}', gender='{self.gender}', major='{self.major}', title='{self.title}')>"


def create_teacher_table(db):
    inspector = inspect(db.engine)
    if not inspector.has_table("Teacher"):
        Teacher.__table__.create(db.engine)


def drop_teacher_table(db):
    inspector = inspect(db.engine)
    if inspector.has_table("Teacher"):
        Teacher.__table__.drop(db.engine)


def add_teacher(db, name, email, gender, major, title):
    existing_teacher = db.session.query(Teacher).filter_by(name=name).first()
    if existing_teacher:
        raise ValueError("Teacher with name already exists.")
    else:
        new_teacher = Teacher(name=name, email=email, gender=gender, major=major, title=title)
        db.session.add(new_teacher)
        db.session.commit()


def find_teacher(db, name):
    teacher = db.session.query(Teacher).filter_by(name=name).first()
    return teacher


def delete_teacher(db, name):
    teacher_to_delete = db.session.query(Teacher).filter_by(name=name).first()
    db.session.delete(teacher_to_delete)
    db.session.commit()


def update_teacher(db, name, email=None, gender=None, major=None, title=None):
    teacher_to_update = db.session.query(Teacher).filter_by(name=name).first()
    if email:
        teacher_to_update.email = email
    if gender:
        teacher_to_update.gender = gender
    if major:
        teacher_to_update.major = major
    if title:
        teacher_to_update.title = title
    db.session.commit()
