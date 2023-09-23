"""
这一部分是评论的表格，不是评论区的。
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import inspect

Base = declarative_base()


class Comment(Base):
    __tablename__ = "Comment"

    id = Column(Integer,  primary_key=True,autoincrement=True)
    teacher_name = Column(String(), nullable=False)
    student_id = Column(Integer(), nullable=False)
    student_name = Column(String(), nullable=False)
    course = Column(String(), nullable=False)
    course_name = Column(String(), nullable =False)
    reply_student = Column(String(), nullable=True)
    content = Column(Text, nullable=False)

    def __init__(self, teacher_name, student_id , student_name, course,course_name, content, reply_student=None):
        self.teacher_name = teacher_name
        self.student_id = student_id
        self.student_name = student_name
        self.course = course
        self.course_name=course_name
        self.content = content
        self.reply_student = reply_student

    def __repr__(self):
        return f"<Comment {self.id}>"


def create_comment_table(db):
    inspector = inspect(db.engine)
    if not inspector.has_table("Comment"):
        Comment.__table__.create(db.engine)


def drop_comment_table(db):
    inspector = inspect(db.engine)
    if inspector.has_table("Comment"):
        Comment.__table__.drop(db.engine)


def add_comment(app,db, teacher_name, student_id, student_name, course,course_name, content, reply_student=None):
    with app.app_context():
        new_comment = Comment(teacher_name, student_id, student_name, course,course_name, content, reply_student)
        print(content)
        db.session.add(new_comment)
        db.session.commit()


def delete_comment(db, comment_id):
    comment = db.session.query(Comment).get(comment_id)
    db.session.delete(comment)
    db.session.commit()


def comment_exists(db, comment_id):
    comment = db.session.query(Comment).get(comment_id)
    return comment


def update_comment(db, comment_id, teacher_name=None, student_id=None ,student_name=None, course=None,course_name=None, content=None, reply_student=None):
    comment = db.session.query(Comment).get(comment_id)
    if teacher_name is not None:
        comment.teacher_name = teacher_name
    if student_name is not None:
        comment.student_name = student_name
    if course is not None:
        comment.course = course
    if content is not None:
        comment.content = content
    if reply_student is not None:
        comment.reply_student = reply_student
    if student_id is not None:
        comment.student_id = student_id
    db.session.commit()

def get_course_comments(app,db,course_id):
    with app.app_context():
        return db.session.query(Comment).filter_by(course=course_id)

