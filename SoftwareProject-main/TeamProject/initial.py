from database.base import *
from threading import Thread
from module.receivedMail import receive_emails
from module.verifyUser import init_mail
from module.ai import init_ai


def initial(app):
    init_db(app)
    #drop_all(app)
    #create_all(app)
    #load_file(app, 'database/class.csv')
    # init_mail()
    # with app.app_context():
    #     username, password = find_Student_account(name="WKY")
    # add_user(name="WKY", username=username, password=password)
    # email_thread = Thread(target=receive_emails,
    #                     args=("WKY",), daemon=True)
    # email_thread.start()
    connection_thread = Thread(target=init_mail, daemon=True)
    connection_thread.start()
    init_ai()
    email_thread = Thread(target=receive_emails, daemon=True)
    email_thread.start()
