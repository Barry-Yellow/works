"""
课程信息
id             自增型变量
课程ID          字符型变量，不可为空
课程名字        字符型变量，不可为空
先修课          课程型变量，可为空
学分           数字型变量，不可为空
院系           字符型变量，不可为空
星级           数字型变量，可为空
时间           日期型变量，不可为空
语言           字符串型变量，不可为空
修课类型        必修课/选修课，不可为空
授课老师        老师型变量，不可为空
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy import inspect

Base = declarative_base()


class Course(Base):
    __tablename__ = "Course"

    id = Column(String(), primary_key=True)
    name = Column(String(), nullable=False)  # 班级的名字，比如生物学原理-01班-双语
    course_id = Column(String(), nullable=False)
    class_name = Column(String(), nullable=False)  # 课程的名字生物学原理
    class_name_en = Column(String(), nullable=False)
    kind = Column(String(), nullable=False)  # 课程性质，比如必修
    classes = Column(String(), nullable=False)  # 课程类别，比如通识必修课
    # 用下面的代码来表示外键间的关系，但这样的约束会让后期对数据的处理更为复杂，建议用name代替掉
    # prior_course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    # prior_course = db.relationship('Course', remote_side=[id], uselist=False)
    # prior_course = Column(String(), nullable=False)
    language = Column(String, nullable=False)
    credit = Column(String(), nullable=False)
    period = Column(String(), nullable=False)  # 学时
    teacher = Column(String(), nullable=False)
    time = Column(String(), nullable=False)
    capacity = Column(Integer(), nullable=False)  # 选课容量
    star = Column(Integer, nullable=True)  # 已选课
    college = Column(String(), nullable=True)  # 已选课

    # 是否是大课或者实验课可以有实现方式，一种是采用以下方式，一种是使用布尔变量
    # experimental_course = db.Column(db.Boolean, nullable=False)
    # experimental_course = Column(Enum("大课", "实验课", name="course_enum"), nullable=False)
    # 老师变量的实现同样可以采取外键之间的关系

    def __init__(self, id, name, course_id, class_name, class_name_en, kind, classes,
                 language, credit, period, teacher, time, capacity, star, college):
        self.id = id
        self.name = name
        self.course_id = course_id
        self.class_name = class_name
        self.class_name_en = class_name_en
        self.kind = kind
        self.classes = classes
        self.language = language
        self.credit = credit
        self.period = period
        self.teacher = teacher
        self.time = time
        self.capacity = capacity
        self.star = star
        self.college = college

    def __repr__(self):
        return f'{{\'name\': {self.name}, \'course_id\': {self.course_id}, \'class_name\': {self.class_name}, \'kind\': {self.kind}, ' \
               f'\'classes\': {self.classes}, \'language\': {self.language}, \'credit\': {self.credit}, ' \
               f'\'period\': {self.period}, \'teacher\': {self.teacher}, \'capacity\': {self.capacity}, \'star\': {self.star}, \'college\': {self.college}}}'


"""
在数据库中创建这个表格
先检查是否存在，不存在就创建
"""


def create_course_table(db):
    inspector = inspect(db.engine)
    if not inspector.has_table("Course"):
        Course.__table__.create(db.engine)


"""
在数据库中删除这个表格
先检查是否存在，存在就删除
"""


def drop_course_table(db):
    inspector = inspect(db.engine)
    if inspector.has_table("Course"):
        Course.__table__.drop(db.engine)


"""
在数据库中添加一门课程
"""


def add_course(db, id, name, course_id, class_name, class_name_en, kind, classes,
               language, credit, period, teacher, time, capacity, star, college):
    course = Course(id=id, name=name, course_id=course_id, class_name=class_name, class_name_en=class_name_en,
                    kind=kind,
                    classes=classes, language=language,
                    credit=credit, period=period, teacher=teacher, time=time, capacity=capacity, star=star,
                    college=college)
    db.session.add(course)
    db.session.commit()


"""
在数据库中删除一门课程
"""


def delete_course_by_id(db, course_id):
    course = db.session.query(Course).get(course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
    else:
        print(f"Course with ID {course_id} not found.")


"""
在数据库中查找所有的课程
"""


def get_all_courses_all(app, db):
    with app.app_context():
        return db.session.query(Course)


def get_all_courses(db):
    return db.session.query(Course).all()


"""
根据课程id查找一门课程
"""


def get_course_by_id(db, course_id):
    return db.session.query(Course).filter_by(id=course_id).first()


"""
更新一门课程的信息
"""


def update_course(db, course_id, name=None, prior_course=None, credit=None, star=None,
                  course_time=None,
                  language=None, experimental_course=None, course_teacher=None, college=None):
    course = db.session.query(Course).get(course_id)
    if not course:
        print(f"Course with ID {course_id} not found.")
        return

    if name is not None:
        course.name = name
    if prior_course is not None:
        course.prior_course = prior_course
    if credit is not None:
        course.credit = credit
    if college is not None:
        course.college = college
    if star is not None:
        course.star = star
    if course_time is not None:
        course.course_time = course_time
    if language is not None:
        course.language = language
    if experimental_course is not None:
        course.experimental_course = experimental_course
    if course_teacher is not None:
        course.course_teacher = course_teacher

    db.session.commit()


"""
    根据学院、名称、老师
"""
