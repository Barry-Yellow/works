from flask import Blueprint, request, jsonify

from module.receivedMail import get_brif, add_user
from module.verifyUser import send_verify_code, check_verify
from database.base import add_email_account

mail = Blueprint('mail', __name__)


@mail.route('/')
def hello():
    return '你好'


# 参数信息较多，建议改用POS方法
@mail.route('/add_account', methods=['GET'])
def add_account():
    name = request.args.get("name")
    print("NAME: ", name)
    email = request.args.get("email")
    print("EMAIL: ", email)
    email_password = request.args.get("email_password")
    print("EMAIL PASSWORD: ", email_password)
    self_intro = request.args.get("self_intro")
    print("SELF INTRO: ", self_intro)
    gpt_key = request.args.get("gpt_key")
    print("GPT KEY: ", gpt_key)

    # 返回值为错误的时候，可能是已经存在用户或者添加失败
    result = add_email_account(name=name, email=email, email_password=email_password,
                               self_intro=self_intro, gpt_key=gpt_key)
    if result:
        add_user(name=name, user_name=email, pass_word=email_password,
                 intro=self_intro, key=gpt_key)
        return "Success"
    else:
        return "The is an error while adding user account."


# POST请求方法
# @mail.route('/add_account', methods=['POST'])
# def add_account():
#     name = request.form.get("name")
#     email = request.form.get("email")
#     email_password = request.form.get("email_password")
#     self_intro = request.form.get("self_intro")
#     gpt_key = request.form.get("gpt_key")
#
#     add_email_account(name=name, email=email, email_password=email_password,
#                       self_intro=self_intro, gpt_key=gpt_key)
#     return "add success"


@mail.route('/email_brif', methods=['GET'])
def email_message():
    name = request.args.get("name")
    email_content, email_importance = get_brif(name)
    if email_content == "":
        print('no return1')
        if email_importance == "":
            print('no return2')
            return "There is an error while searching for content"
    # print("New requirement received")
    # print(email_content, email_importance)
    email_data = {
        'importance': email_importance,
        'content': email_content
    }
    print(jsonify(email_data))
    return jsonify(email_data)


@mail.route('/verify_by_mail', methods=['GET'])
def verify_request():
    # email = request.form.get("email")    # POST
    email = request.args.get("email")  # GET
    if send_verify_code(email):
        return "Check your email"
    else:
        return "There is an error while trying to send an verify code"


@mail.route('/verify_confirm_code', methods=['GET'])
def verify_code():
    code = request.args.get("code")  # GET
    email = request.args.get("email")  # GET
    if check_verify(email, code):
        return "That is right, Hello World!"
    return "You may want to check your email again, just to make sure you didn't write the code wrong"
