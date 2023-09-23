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


class AI(Base):
    __tablename__ = "AI"

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    gpt_key = Column(String(), nullable=True)

    def __init__(self, name, gpt_key):
        self.name = name
        self.gpt_key = gpt_key

    def __repr__(self):
        return '<Student %r>' % self.name


"""
在数据库中创建这个表格
先检查是否存在，不存在就创建
"""


def create_ai_table(db):
    inspector = inspect(db.engine)
    if not inspector.has_table("AI"):
        AI.__table__.create(db.engine)


"""
在数据库中删除这个表格
先检查是否存在，存在就删除
"""


def drop_ai_table(db):
    inspector = inspect(db.engine)
    if inspector.has_table("AI"):
        AI.__table__.drop(db.engine)


"""
在数据库中添加一个学生的邮件账号
"""


def add_ai_user_account(db, name, gpt_key):
    if name is None:
        return "Name can not be None"
    if gpt_key is None:
        return "Gpt key can not be None"

    existing_account = db.session.query(AI).filter_by(name=name).first()
    if existing_account:
        raise ValueError("Student with name already exists.")
    else:
        new_account = AI(name=name, gpt_key=gpt_key)
        db.session.add(new_account)
        db.session.commit()


"""
在数据库中删除一个学生
"""


def delete_ai_student(db, name):
    existing_account = db.session.query(AI).filter_by(name=name).first()
    if existing_account:
        db.session.delete(existing_account)
        db.session.commit()


"""
在数据库中查询一个学生
"""


def check_ai_student(db, name):
    student = db.session.query(AI).filter_by(name=name).first()
    return student is not None


def find_ai_student(db, name):
    student = db.session.query(AI).filter_by(name=name).first()
    return student


def get_ai_all(db):
    return db.session.query(AI).all()


def find_ai_key(db, name):
    student = db.session.query(AI).filter_by(name=name).first()
    return student.gpt_key


"""
修改一个学生的信息
"""


def modify_ai_student(db, name, new_name=None, new_gpt_key=None):
    student = db.session.query(AI).filter_by(name=name).first()
    if new_name is not None:
        student.name = new_name
    if new_gpt_key is not None:
        student.gpt_key = new_gpt_key

    db.session.commit()
