import os

import flask
from flask import Flask, flash, session, request, redirect, url_for
from flask import render_template
from api.conf import config
from flask_oidc import OpenIDConnect
from api.database import Database
from flask_cors import CORS
import json
from api.action import User

app = Flask(__name__)
config = config.Config()
db = Database()

# 初始化
db.init_tables()
config.init_oidc_json()

app.config.update({
    'SECRET_KEY': config.secret_key,  # Replace with your own secret key
    'OIDC_CLIENT_SECRETS': f'{os.path.dirname(__file__)}/api/conf/client_secrets.json',
    'OVERWRITE_REDIRECT_URI': f'{config.redirect_uri}/authorize',
    'OIDC_COOKIE_SECURE': True,
    'OIDC_SCOPES': ['openid', 'email', 'profile']  # Specify the scopes you need
})

oidc = OpenIDConnect(app)
CORS(app, resources=r'/*')




@app.route('/')
@oidc.require_login
def login():
    username = oidc.user_getfield('email').split('@')[0]
    if username not in db.get_user():
        if username == config.admin_name:
            db.add_user(username, oidc.user_getinfo(['pofile'])['name'],
                        oidc.user_getfield('email'), 'admin')
        else:
            db.add_user(username, oidc.user_getinfo(['pofile'])['name'],
                        oidc.user_getfield('email'))
    if username != config.admin_name:
        return redirect(url_for('manage'))
    else:
        return redirect(url_for('admin'))


@app.route('/manage', methods=["GET", "POST"])
def manage():  # put application's code here
    if not oidc.user_loggedin:
        return redirect(url_for('login'))
    try:
        data = json.loads(request.form.get('data'))
        action = data['action']
        print(data)

        action = User(oidc.user_getinfo(['pofile'])['name'], data)
        print(action.action())
    except Exception as e:
        print(f"Error: {e}")

    return render_template('manage.html', data_dict=db.get_record(oidc.user_getinfo(['pofile'])['name']),
                           domain=oidc.user_getinfo(['pofile'])['name'], domain_list=db.get_domain(),
                           user=oidc.user_getfield('email').split('@')[0])


@app.route('/admin', methods=["GET", "POST"])
@oidc.require_login
def admin():
    username = oidc.user_getfield('email').split('@')[0]
    if username != config.admin_name:
        return redirect(url_for('manage'))
    try:
        data = json.loads(request.form.get('data'))
        action = data['action']
        print(data)

        #action = User(oidc.user_getinfo(['pofile'])['name'], data)
        #print(action.action())
    except Exception as e:
        pass
    return render_template('admin.html', data_dict=db.get_all_record(),
                           user_list=db.get_user(), domain_list=db.get_domain(),
                           user=username)


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
