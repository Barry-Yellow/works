import csv
import re
from flask_sqlalchemy import SQLAlchemy
from .Course import create_course_table, drop_course_table, add_course, get_all_courses, get_course_by_id, \
    get_all_courses_all
from .Comment import create_comment_table, drop_comment_table, get_course_comments, add_comment
from .Student import create_student_table, drop_student_table, find_student_by_id, add_student_email, check_student, \
    add_student, get_student_by_email, modify_student
from .Teacher import create_teacher_table, drop_teacher_table
from .Time import create_time_table, drop_time_table, add_time, find_time_byname, find_time_byid
from .algorithm import back_tracking
from .Email import *
from .AI import *

db = SQLAlchemy()


#

def init_db(app):
    """
    1.配置格式：数据库类型+使用的模块://用户名:密码@服务器ip地址:端口/数据库
    2.如果设置成 True，SQLAlchemy 将会记录所有发到标准输出(stderr)的语句，可以用于调试
    3.用于设定数据库连接池的大小，默认值为10
    4.设置在连接池到达上限之后可以创建的最大连接数
    5.是否检测数据库的修改
    6.设置链接密钥
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://barry:123456@localhost:5432/software'
    # app.config['SQLALCHEMY_ECHO'] = True
    # app.config['SQLALCHEMY_POOL_SIZE'] = 10
    # app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'xxx'

    global localApp
    localApp = app
    db.init_app(app)
    check_all(app)


def create_all(app):
    with app.app_context():
        create_course_table(db)
        create_time_table(db)
        create_student_table(db)
        create_comment_table(db)


def drop_all(app):
    with app.app_context():
        drop_course_table(db)
        drop_time_table(db)
        drop_student_table(db)
        drop_comment_table(db)


def check_all(app):
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table("Email"):
            create_email_table(db)
        if not inspector.has_table("AI"):
            create_ai_table(db)


"""
在这里加入其他的方法，将他们封装一层后传给具体的每个类
"""


def load_course(app, data):
    with app.app_context():
        for d in data:
            time = ' '.join(d['time'])
            add_course(db, d['id'], d['name'], d['course_id'], d['class_name'], d['class_name_en'], d['kind'],
                       d['classes'], d['language'], d['credit'], d['period'], d['teacher'], time,
                       int(d['capacity']), int(d['star']), d['department'])


def load_time(app, data):
    with app.app_context():
        for d in data:
            for t in d['time']:
                add_time(db, d['id'], d['class_name'], t)


def load_file(app, filename):
    with app.app_context():
        with open(filename, 'r', encoding='GBK') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            new_data = list()
            for d in data:
                if d not in new_data:
                    new_data.append(d)
            for d in new_data:
                s = d['information']
                teacher = []
                pattern1 = r'<a.*?>(.*?)</a>'
                matches1 = re.findall(pattern1, s)
                for match in matches1:
                    teacher.append(match)
                d['teacher'] = ' '.join(teacher)

                time = []
                new_time = []
                pattern2 = r'星期(.)第(\d+)-(\d+)节'
                matches2 = re.findall(pattern2, s)
                for match in matches2:
                    full_match = ''.join(('星期', match[0], '第', match[1], '-', match[2], '节'))
                    time.append(full_match)
                for t in time:
                    if t not in new_time:
                        new_time.append(t)
                d['time'] = new_time
            # new_data.sort(key=data.index)
            load_course(app, new_data)
            load_time(app, new_data)


"""
    下面是app的url访问中需要直接用到的方法
"""


def get_whole_courses():
    return get_all_courses(db)


def get_course(data):
    new_data = []
    for d in data:
        route = []
        for c in d:
            route.append(get_course_by_id(db, c))
        new_data.append(route)
    return new_data


def select_course(courses):
    target_courses = []
    for course in courses:
        target_courses.append(find_time_byname(db, course))
    return back_tracking(target_courses)


def get_all_courses_base(app):
    with app.app_context():
        return get_all_courses_all(app, db)


def get_student_by_id_base(app, student_id):
    x = find_student_by_id(app, db, student_id)
    return x


def get_comments_by_course_base(app, course_id):
    x = get_course_comments(app, db, course_id)
    return x


def add_comment_base(app, teacher_name, student_id, student_name, course, course_name, content, reply_student=None):
    x = add_comment(app, db, teacher_name, student_id, student_name, course, course_name, content, reply_student=None)
    return x


def get_course_by_id_base(app, course_id):
    with app.app_context():
        x = get_course_by_id(db, course_id)
        return x


"""
邮箱功能要用的两个方法
"""


def add_email_account(name, email, email_password, self_intro, gpt_key):
    if not check_mail_student(db, name):
        add_mail_user_account(db=db, name=name, email=email, email_password=email_password,
                              self_intro=self_intro, gpt_key=gpt_key)
        return check_mail_student(db, name)
    else:
        return False


def get_all_email_account():
    with localApp.app_context():
        return get_mail_all(db)


def add_ai_account(name, gpt_key):
    if not check_ai_student(db, name):
        add_ai_user_account(db=db, name=name, gpt_key=gpt_key)
        return check_ai_student(db, name)
    else:
        return False


def get_all_ai_account():
    with localApp.app_context():
        return get_ai_all(db)


def get_student_by_email_base(app, email_address):
    x = get_student_by_email(app, db, email_address)
    return x


def modify_student_base(app, student_id, username, name, password, gender, major, email, email_password):
    modify_student(app, db, student_id, username, name, password, gender, major, email, email_password)
    return


def add_student_base(app, id, username, name, password, gender, major, email=None, email_password=None):
    x = add_student(app, db, id, username, name, password, gender, major, email, email_password)

def change_ai_account(name, gpt_key):
    modify_ai_student(db, name, name, gpt_key)
    return find_ai_key(db, name) == gpt_key
