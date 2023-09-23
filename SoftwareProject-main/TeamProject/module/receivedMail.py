import zmail
from time import sleep
import openai
from threading import Thread
from database.base import get_all_email_account

"""
username用于存储用户的邮箱名，必须是腾讯企业邮箱的账户名
password对应邮箱的密码
user_server存储在添加用户时创建的与邮箱服务器的连接
user_intro用于存储用户对自己的简介，用于生成对邮箱的分析过滤
user_key用于存储用户的open_ai.key
email_brif用于存储对用户最近一封邮件的分析摘要
email_importance存储对邮箱的分级
email_id用于判断最新的邮件是否时最新的
email_all用于存储一定数量的email
"""

username = {}
password = {}
user_server = {}
user_intro = {}
user_key = {}
email_brif = {}
email_importance = {}
email_id = {}
email_all = {}


def init_user():
    user_list = get_all_email_account()
    for user in user_list:
        print("add user: ")
        add_user(user.name, user.email, user.email_password, user.self_intro, user.gpt_key)
    print(email_brif.keys())


def add_user(name, user_name, pass_word, intro, key):
    username[name] = user_name
    password[name] = pass_word
    user_intro[name] = intro
    user_key[name] = key

    user_server[name] = \
        zmail.server(username=user_name, password=pass_word, pop_host='pop.exmail.qq.com', pop_port=995)


def get_brif(name):
    print(name)
    print(email_importance.keys())
    if email_brif.get(name):
        if email_importance.get(name):
            return email_brif.get(name), email_importance.get(name)
    return "", ""


def get_mail(name):
    email_list = []
    server = user_server[name]
    email_latest = server.get_latest()
    for i in range(email_latest['id'] - 4, email_latest['id'] + 1):
        email = server.get_mail(i)
        email_list.append(email)
    email_all[name] = email_list


def response_ai(name, email):
    email_subject = email['subject']
    email_content = email['content_text'][0]
    email_content = email_content.replace("\r\n", "")

    email_importance[name] = abstract_ai(name, email_subject, email_content)
    email_brif[name] = summary_ai(name, email_subject, email_content)
    print(name)
    print(email_importance[name])
    print(email_brif[name])


def abstract_ai(name, email_subject, email_content):
    self_intro = user_intro[name]
    openai.api_key = user_key[name]
    conversation = []

    content = self_intro + email_subject + email_content

    conversation.append({
        'role': 'system',
        'content': content
    })
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation
    )
    return int(response.choices[-1].message.content[0:1])


def summary_ai(name, email_subject, email_content):
    conversation = []
    openai.api_key = user_key[name]
    summary_require = "我希望你对下面这封邮件生成一份简单的摘要，不要超过五十个字，用中文回答："
    summary_content = summary_require + email_subject + email_content
    conversation.append({
        'role': 'system',
        'content': summary_content
    })
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation
    )
    return response.choices[-1].message.content


def receive_emails():
    init_user()
    while True:
        for name in username.keys():
            latest_mail = user_server[name].get_latest()
            if latest_mail:
                if name in email_id.keys():
                    if latest_mail['id'] > email_id[name]:
                        email_id[name] = latest_mail['id']
                        user_thread = Thread(target=response_ai, args=(name, latest_mail), daemon=True)
                        user_thread.start()
                else:
                    email_id[name] = latest_mail['id']
                    user_thread = Thread(target=response_ai, args=(name, latest_mail), daemon=True)
                    user_thread.start()

        # Check for new emails every 10 seconds
        sleep(10)
