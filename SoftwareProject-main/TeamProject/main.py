from flask import Flask, jsonify, request

from database import Course
from database.base import *
import database.Course
from initial import initial
import json
import ssl
from flask import Blueprint
from request.mailRequest import mail
from request.aiRequest import ai
from module.verifyUser import send_verify_code, check_verify

app = Flask(__name__)
"""
运行项目前安装必要的modules
pip install flask
pip install flask_sqlalchemy
pip install psycopg2-binary
pip install sqlalchemy 
"""


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route('/get_data', methods=['GET'])
def get_data():
    # 构造 JSON 数据段
    data = get_whole_courses()
    course_data = [
        {'name': d.name, 'course_id': d.course_id, 'class_name': d.class_name, 'kind': d.kind, 'classes': d.classes,
         'language': d.language, 'credit': d.credit, 'period': d.period, 'teacher': d.teacher,
         'time': d.time, 'capacity': d.capacity, 'star': d.star, 'college': d.college} for d in data]

    json_return = {'data': course_data}
    # 返回 JSON 响应
    return jsonify(json_return)


@app.route('/select_class', methods=['GET'])
def select_class():
    courses = request.args.getlist('courses[]')
    data, features = select_course(courses)
    new_data = get_course(data)
    final_data = []
    for index in range(len(new_data)):
        da = new_data[index]
        course_data = [
            {'name': d.name, 'course_id': d.course_id, 'class_name': d.class_name, 'kind': d.kind, 'classes': d.classes,
             'language': d.language, 'credit': d.credit, 'period': d.period, 'teacher': d.teacher,
             'time': d.time, 'capacity': d.capacity, 'star': d.star, 'college': d.college} for d in da]
        final_data.append({'plan': course_data, 'features': features[index]})
    json_return = {'data': final_data}
    # 返回 JSON 响应
    return jsonify(json_return)


"""
typesrcipt解析这个json对象：

interface Person {
  name: string;
  age: string;
}
const peopleJSON = '{"people": [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}, {"name": "Charlie", "age": 35}]}';
const parsedJSON = JSON.parse(peopleJSON);
const people: Person[] = parsedJSON.people;
console.log(people);
"""


@app.route('/post_data', methods=['POST'])
def post_data():
    # 获取 POST 请求的参数
    name = request.form.get('name')
    age = request.form.get('age')

    # 构造 JSON 数据段
    data = {
        'name': name,
        'age': age
    }

    # 返回 JSON 响应
    return jsonify(data)


"""
    评论区部分总共三个方法
    1.针对对应的约束条件，显示其课程列表 @ /getCourseList
    2.针对某个课程，显示其评论区的条目 @ /getCourseComments
    3.针对某个课程，某个用户post其评论 @ /postComment
"""
"""
显示课程表列表
"""


@app.route('/getCourseList', methods=['GET'])
def get_course_list():
    student_id = request.args.get('id')
    college = request.args.get('college')
    courseName = request.args.get('course')
    teacher = request.args.get('teacher')
    queryList = get_all_courses_base(app)
    if student_id:
        if not get_student_by_id_base(app, student_id):
            return jsonify({'response': 'wrongID'})
    else:
        return jsonify({'response': 'noID'})
    if college:
        queryList = queryList.filter(Course.Course.college.like('%{}%'.format(college)))
    if courseName:
        queryList = queryList.filter(Course.Course.class_name.like('%{}%'.format(courseName)))
    if teacher:
        queryList = queryList.filter(Course.Course.teacher.like('%{}%'.format(teacher)))
    courses = queryList.all()
    result = [{'id': c.id, 'name': c.name, 'course_id': c.course_id, 'class_name': c.class_name,
               'class_name_en': c.class_name_en, 'kind': c.kind, 'classes': c.classes, 'language': c.language,
               # 'score': c.score,
               'credit': c.credit, 'period': c.period, 'capacity': c.capacity, 'star': c.star,
               'college': c.college, 'teacher': c.teacher, 'time': c.time} for c in courses]
    result = json.dumps(result, ensure_ascii=False)
    print(result)
    return result


@app.route('/getCourseComments', methods=['GET'])
def get_comments():
    Course_id = request.args.get('course_id')
    comments = get_comments_by_course_base(app, course_id=Course_id).all()
    result = [{'id': c.id, 'teacher_name': c.teacher_name, 'student_id': c.student_id, 'student_name': c.student_name,
               'course_id': c.course, 'course_name': c.course_name, 'reply_student': c.reply_student,
               'content': c.content} for c in comments]
    x = json.dumps(result, ensure_ascii=False)
    print(x)
    return x


@app.route('/postComment', methods=['POST'])
def post_comment():
    # # 获取 POST 请求的参数
    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')
    content = request.form.get('content')
    reply = request.form.get('reply_to')
    teacher_name = '--'
    student_name = '--'
    cs = get_course_by_id_base(app, course_id)
    st = get_student_by_id_base(app, student_id)
    if cs:
        teacher_name = get_course_by_id_base(app, course_id).teacher
        course_name = cs.class_name
    else:
        return jsonify({'response': 'invalid course_id'})
    if st:
        student_name = get_student_by_id_base(app, student_id).name
    if student_id and student_name and course_id and content:
        add_comment_base(app, teacher_name, student_id, student_name, course_id, course_name, content, reply)
        comments = get_comments_by_course_base(app, course_id=course_id).all()
        result = [
            {'id': c.id, 'teacher_name': c.teacher_name, 'student_id': c.student_id, 'student_name': c.student_name,
             'course_id': c.course, 'course_name': c.course_name, 'reply_student': c.reply_student,
             'content': c.content} for c in comments]
        x = json.dumps(result, ensure_ascii=False)
        return x
    else:
        return jsonify({'response': 'invalid args'})


"""
    这个方法用来注册，每一个元素都不能缺少
    1. 如果有元素缺失，返回 'state': 'invalid information'
    2. 如果用户已存在，返回 'state': 'user exists'
    3. 如果前两个条件不满足，则注册
"""


@app.route('/register', methods=['POST'])
def register():
    student_id = request.form.get('id')
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    gender = request.form.get('gender')
    major = request.form.get('major')
    email = request.form.get('email')
    email_password = request.form.get('email_password')
    if not student_id or not username or not name or not password or not gender or not major or not email_password or not email:
        print('invalid information')
        return jsonify({'state': 'invalid information'})
    st = get_student_by_id_base(app, student_id)
    if st:
        print('user exists')
        return jsonify({'state': 'id exists or name exist'})
    if not check_verify(email, email_password):
        return jsonify({'state': 'wrong verify code'})
    try:
        add_student_base(app, student_id, username, name, password, gender, major, email, email_password)
        print('succeed')
        return jsonify({'state': 'succeed'})
    except Exception as e:
        print(e)
        return jsonify({'state': 'invalid information'})



@app.route('/login', methods=['POST'])
def login():
    student_id = request.form.get('id')
    password = request.form.get('password')
    email_address = request.form.get('email_address')
    if email_address:
        pass
    elif student_id and password:
        st = get_student_by_id_base(app, student_id)
        if not st:
            return jsonify({'state': 'no such user'})
        if st.password != password:
            return jsonify({'state': 'wrong password'})
        c = st
        return jsonify({'state': 'succeed', 'id': c.id, 'password': c.password, 'username': c.username, 'name': c.name,
                        'major': c.major,
                        'gender': c.gender, 'email': c.email, 'email_password': c.email_password})
        pass
    return jsonify({'state': 'no id or password'})


@app.route('/login_by_email', methods=['POST'])
def login_by_email():
    email_address = request.form.get('email_address')
    st = get_student_by_email_base(app, email_address)
    if st:
        if send_verify_code(email_address):
            return jsonify({'state': 'send succeed'})
        else:
            return jsonify({'state': 'wrong address'})
    else:
        return jsonify({'state': 'email address don\'t exist'})


@app.route('/register_by_email', methods=['POST'])
def regiter_by_email():
    email_address = request.form.get('email_address')
    st = get_student_by_email_base(app, email_address)
    if st:
        return jsonify({'state': 'email exists'})
    if send_verify_code(email_address):
       return jsonify({'state': 'send succeed'})
    else:
        return jsonify({'state': 'wrong emailaddress'})

@app.route('/login_by_verify_code', methods=['POST'])
def verify_by_email():
    email_address = request.form.get('email_address')
    code = request.form.get('verify_code')
    st = get_student_by_email_base(app, email_address)
    if not st:
        return jsonify({'state': 'wrong email address'})
    c = st
    if check_verify(email_address, code):
        return jsonify({'state': 'succeed', 'id': c.id, 'password': c.password, 'username': c.username, 'name': c.name,
                        'major': c.major,
                        'gender': c.gender, 'email': c.email, 'email_password': c.email_password})
    else:
        return jsonify({'state': 'wrong code'})


@app.route('/modify', methods=['POST'])
def modify_st():
    student_id = request.form.get('id')
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    gender = request.form.get('gender')
    major = request.form.get('major')
    email = request.form.get('email')
    email_password = request.form.get('email_password')
    c = get_student_by_id_base(app, student_id)
    if c.password != password:
        return jsonify({'state': 'wrong password'})
    try:
        modify_student_base(app, student_id, username, name, password, gender, major, email, email_password)
        c = get_student_by_id_base(app, student_id)
        return jsonify({'state': 'succeed', 'id': c.id, 'password': c.password, 'username': c.username, 'name': c.name,
                        'major': c.major,
                        'gender': c.gender, 'email': c.email, 'email_password': c.email_password})
    except Exception as e:
        print(e)
        return jsonify({'state': 'invalid information'})


if __name__ == '__main__':
    # 本地调试时使用
    # app.run()

    # init_db(app)
    initial(app)
    # 将服务公开至全网使用
    app.register_blueprint(mail, url_prefix='/mail')
    app.register_blueprint(ai, url_prefix='/ai')
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'),threaded=True)
"""
    评论区部分总共三个方法
    1.针对对应的课程，显示其评论区

"""

"""
要使用PyCharm连接GitHub仓库进行多人协作，您可以遵循以下步骤：
1.在GitHub上创建一个新的仓库，或者加入一个已经存在的仓库。
2.将仓库的URL复制到剪贴板中。
3.在PyCharm中打开您的项目，然后从菜单栏中选择“VCS”>“Git”>“Clone”。
4.在弹出的窗口中，将GitHub仓库的URL粘贴到“URL”字段中，并选择您要将仓库克隆到本地计算机的目录。然后单击“Clone”按钮。
5.在PyCharm中打开您的项目后，您可以开始编写代码并将其提交到仓库。在PyCharm中，您可以使用“VCS”>“Git”>“Commit Changes”来提交代码更改。
6.如果您希望与其他人协作，您可以邀请他们加入仓库并为项目做出贡献。您可以在GitHub仓库的设置页面中添加合作者，以便其他人可以访问和编辑仓库。
7.您可以在PyCharm中使用“VCS”>“Git”>“Push”将您的更改推送到GitHub仓库中。如果其他人已经对仓库进行了更改，您需要先将其拉取到本地计算机上，然后再推送您的更改。
8.通过这些步骤，您可以使用PyCharm连接GitHub仓库进行多人协作。
"""
