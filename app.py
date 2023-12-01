import logging
import os

import flask
from flask import Flask, session, request, redirect, url_for, jsonify
from flask import render_template
from api.conf import config
from flask_oidc import OpenIDConnect
from api.database import Database
from api.sync import sync_db_record, sync_db_domain_record, sync_db_domain_list
from flask_cors import CORS
import json
from api.action import User, Admin
from api.sync import sync_db_record

app = Flask(import_name=__name__, template_folder='templates', static_folder='static')
config = config.Config()
db = Database()

# 初始化
db.init_tables()
config.init_oidc_json()
sync_db_domain_record()
sync_db_record()
sync_db_domain_list()

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
    username = session['oidc_auth_profile']['email'].split('@')[0]
    if username in db.get_disabled_user():
        return "您的账户已被禁用，请联系管理员"
    if username not in db.get_user():
        if username == config.admin_name:
            db.add_user(username, session['oidc_auth_profile']['name'],
                        session['oidc_auth_profile']['email'], 'admin')
            sync_db_record()
        else:
            db.add_user(username, session['oidc_auth_profile']['name'],
                        session['oidc_auth_profile']['email'])
            sync_db_record()
    db.record_login_time(username)
    if username != config.admin_name:
        return redirect(url_for('manage'))
    else:
        return redirect(url_for('admin'))


@app.route('/manage', methods=["GET", "POST"])
def manage():  # put application's code here
    if not oidc.user_loggedin:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        action = User(session['oidc_auth_profile']['email'].split('@')[0], data)
        status = action.action()
        info = dict()
        info['status'] = status
        return jsonify(info)
    else:
        return render_template('manage.html', data_dict=db.get_record(session['oidc_auth_profile']['name']),
                               domain_list=db.get_domain(), user=session['oidc_auth_profile']['email'].split('@')[0])


@app.route('/admin', methods=["GET", "POST"])
@oidc.require_login
def admin():
    username = session['oidc_auth_profile']['email'].split('@')[0]
    if username != config.admin_name:
        return redirect(url_for('manage'))
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        action = Admin(session['oidc_auth_profile']['email'].split('@')[0], data)
        status = action.action()
        info = dict()
        info['status'] = status
        return jsonify(info)
    else:
        return render_template('admin.html', data_dict=db.get_all_record(),
                               user_list=db.get_user(), domain_list=db.get_domain(),
                               user=username, user_dict=db.get_all_user(), setting=config.get_all_setting())


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
