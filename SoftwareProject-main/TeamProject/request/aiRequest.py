from flask import Blueprint, request, jsonify

from module.ai import use_ai, add_user, change_user, refresh
from database.base import add_ai_account

ai = Blueprint('ai', __name__)


@ai.route('/')
def hello():

    return '你好'


# 参数信息较多，建议改用POS方法
@ai.route('/add_account', methods=['GET'])
def add_account():
    name = request.args.get("name")
    gpt_key = request.args.get("gpt_key")

    # 返回值为错误的时候，可能是已经存在用户或者添加失败
    result = add_ai_account(name=name, gpt_key=gpt_key)
    if result:
        add_user(name, gpt_key)
        return "Success"
    else:
        return "The is an error while adding user account."


@ai.route('/ai_chat', methods=['GET'])
def email_message():
    name = request.args.get("name")
    content = request.args.get("content")
    response = use_ai(name, content)
    print(response)
    return jsonify(response)


@ai.route('/modify_account', methods=['GET'])
def modify_account():
    name = request.args.get("name")
    gpt_key = request.args.get("gpt_key")

    if change_user(name, gpt_key):
        return "Modify Success"
    return "There is an error while changing account"


@ai.route('/refresh', methods=['GET'])
def refresh_conversation():
    name = request.args.get("name")
    refresh(name)
    return "Success"
