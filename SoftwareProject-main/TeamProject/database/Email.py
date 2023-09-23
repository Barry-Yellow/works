"""
学生类型
id      自增变量，创建实例时不需要传入
姓名：   字符串，长度不定，不可为空
邮箱：   字符串，长度不定，不可为空
邮箱密码：字符串，长度不定，不可为空
最新邮件：字符串，长度不定，可为空
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import inspect

Base = declarative_base()


class Email(Base):
    __tablename__ = "Email"

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    email_password = Column(String(), nullable=False)
    newest_email = Column(String(), nullable=True)
    self_intro = Column(String(), nullable=True)
    gpt_key = Column(String(), nullable=True)

    def __init__(self, name, email, email_password, newest_email, self_intro, gpt_key):
        self.name = name
        self.email = email
        self.email_password = email_password
        self.newest_email = newest_email
        self.self_intro = self_intro
        self.gpt_key = gpt_key

    def __repr__(self):
        return '<Student %r>' % self.name


"""
在数据库中创建这个表格
先检查是否存在，不存在就创建
"""


def create_email_table(db):
    inspector = inspect(db.engine)
    if not inspector.has_table("Email"):
        Email.__table__.create(db.engine)


"""
在数据库中删除这个表格
先检查是否存在，存在就删除
"""


def drop_email_table(db):
    inspector = inspect(db.engine)
    if inspector.has_table("Email"):
        Email.__table__.drop(db.engine)


"""
在数据库中添加一个学生的邮件账号
"""


def add_mail_user_account(db, name, email, email_password, self_intro, gpt_key, newest_email=None):
    if name is None:
        return "Name can not be None"
    if email is None:
        return "Email account can not be None"
    if email_password is None:
        return "Email password can not be None"
    if self_intro is None:
        return "You need to have an self introduction"
    if gpt_key is None:
        return "Gpt key can not be None"

    existing_account = db.session.query(Email).filter_by(name=name).first()
    if existing_account:
        raise ValueError("Student with name already exists.")
    else:
        new_account = Email(name=name, email=email, email_password=email_password,
                            newest_email=newest_email, self_intro=self_intro, gpt_key=gpt_key)
        db.session.add(new_account)
        db.session.commit()


"""
在数据库中删除一个学生
"""


def delete_mail_student(db, name):
    existing_account = db.session.query(Email).filter_by(name=name).first()
    if existing_account:
        db.session.delete(existing_account)
        db.session.commit()


"""
在数据库中查询一个学生
"""


def check_mail_student(db, name):
    student = db.session.query(Email).filter_by(name=name).first()
    return student is not None


def find_mail_student(db, name):
    student = db.session.query(Email).filter_by(name=name).first()
    return student


def get_mail_all(db):
    return db.session.query(Email).all()



"""
修改一个学生的信息
name = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    email_password = Column(String(), nullable=False)
    newest_email = Column(String(), nullable=True)
    self_intro = Column(String(), nullable=True)
    gpt_key = Column(String(), nullable=True)
"""


def modify_mail_student(db, name, new_email=None, new_email_password=None, new_self_intro=None, new_gpt_key=None):
    student = db.session.query(Email).filter_by(name=name).first()
    if new_email is not None:
        student.email = new_email
    if new_email_password is not None:
        student.name = new_email_password
    if new_self_intro is not None:
        student.password = new_self_intro
    if new_gpt_key is not None:
        student.gender = new_gpt_key

    db.session.commit()
