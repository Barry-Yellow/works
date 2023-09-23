"""
学生类型
id      自增变量，创建实例时不需要传入
用户名   字符串，长度不定，不可为空
姓名：   字符串，长度不定，不可为空
密码：   字符串，长度不定，不可为空
性别：   两种情况，男或者女，可为空
专业：   字符串，长度不定，可以为空
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import inspect

Base = declarative_base()


class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key=True)
    username = Column(String(), nullable=False)
    name = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    gender = Column(String(), nullable=True)
    major = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    email_password = Column(String(), nullable=False)

    def __init__(self, id, username, name, password, gender, major, email, email_password):
        self.id = id
        self.username = username
        self.name = name
        self.password = password
        self.gender = gender
        self.major = major
        self.email = email
        self.email_password = email_password

    def __repr__(self):
        return '<Student %r>' % self.name


"""
在数据库中创建这个表格
先检查是否存在，不存在就创建
"""


def create_student_table(db):
    inspector = inspect(db.engine)
    if not inspector.has_table("Student"):
        Student.__table__.create(db.engine)


"""
在数据库中删除这个表格
先检查是否存在，存在就删除
"""


def drop_student_table(db):
    inspector = inspect(db.engine)
    if inspector.has_table("Student"):
        Student.__table__.drop(db.engine)


"""
在数据库中添加一个学生
"""


def add_student(app, db, id, username, name, password, gender, major, email=None, email_password=None):
    if not (username or id or name or password or gender or major):
        print('info wrong')
        return
    with app.app_context():
        new_student = Student(id=id, username=username, name=name,
                              password=password, major=major, gender=gender, email=email, email_password=email_password)
        db.session.add(new_student)
        db.session.commit()


"""
在数据库中删除一个学生
"""


def delete_student(db, name):
    student = db.session.query(Student).filter_by(name=name).first()
    db.session.delete(student)
    db.session.commit()


"""
在数据库中查询一个学生
"""


def check_student(db, name):
    student = db.session.query(Student).filter_by(name=name).first()
    return student


"""
修改一个学生的信息
"""


def modify_student(app, db,student_id, username, name, password, gender, major, email, email_password):
    student = db.session.query(Student).filter_by(id=student_id).first()
    if username is not None:
        student.username = username
    if name is not None:
        student.name = name
    if password is not None:
        student.password = password
    if gender is not None:
        student.gender = gender
    if major is not None:
        student.major = major
    if email is not None:
        student.email = email
    if email_password is not None:
        student.email_password = email_password
    db.session.commit()


def find_student_by_id(app, db, student_id):
    with app.app_context():
        return db.session.query(Student).filter_by(id=student_id).first()


"""
邮箱要用到的几个方法
"""


def add_student_email(db, name, email, email_password, newest_email=None):
    if name is None:
        return "Name can not be None"

    existing_student = db.session.query(Student).filter_by(name=name).first()
    if existing_student:
        raise ValueError("Student with name already exists.")
    else:
        new_student = Student(
            name=name, email=email, email_password=email_password, newest_email=newest_email)
        db.session.add(new_student)
        db.session.commit()


def check_student(db, name):
    student = db.session.query(Student).filter_by(name=name).first()
    return student

def get_student_by_email(app,db,email_address):
    with app.app_context():
        return db.session.query(Student).filter_by(email=email_address).first()

