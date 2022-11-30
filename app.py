import json

from flask import Flask, render_template, redirect, session, url_for
from auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report
from basket.route import blueprint_order
from blueprint_edit.route import blueprint_edit
from typing import List, Callable
from access import login_required, group_required


app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/zaproses')
app.register_blueprint(blueprint_report, url_prefix='/reports')
app.register_blueprint(blueprint_order, url_prefix='/order')
app.register_blueprint(blueprint_edit, url_prefix='/edit')


app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['report_list'] = json.load(open('data_files/report_list.json'))
app.config['report_url'] = json.load(open('data_files/report_url.json'))
app.config['cache_config'] = json.load(open('data_files/cache.json'))

with open('data_files/access.json', 'r') as f:
    access_config = json.load(f)
    app.config['access_config'] = access_config


@app.route('/', methods=['GET', 'POST'])
def menu_choice():
    if 'user_id' in session:
        if session.get('user_group', None):
            return render_template('internal_user_menu.html')
        else:
            return render_template('external_user_menu.html')
    else:
        return redirect(url_for('blueprint_auth.start_auth'))


@app.route('/exit')
def exit_func():
    session.clear()
    return 'До свиданья, заходите к нам еще'


def add_blueprint_access_handler(app: Flask, blueprint_names: List[str], handler: Callable) -> Flask:
    for view_func_name, view_func in app.view_functions.items(): #цикл по всем доступным обработчикам
        print('view_func_name=', view_func_name)
        print('view_func', view_func)
        view_func_parts = view_func_name.split('.')
        if len(view_func_parts) > 1:
            view_blueprint = view_func_parts[0]
            if view_blueprint in blueprint_names:
                view_func = handler(view_func) # функция оборачивается в декоратор
                app.view_functions[view_func_name] = view_func
    return app


if __name__ == '__main__':
    app = add_blueprint_access_handler(app, ['bp_report', 'bp_query', 'bp_order', 'bp_edit'], group_required)
    app = add_blueprint_access_handler(app, ['bp_report', 'bp_query', 'bp_order', 'bp_edit'], login_required)
    app.run(host='127.0.0.1', port=5001)