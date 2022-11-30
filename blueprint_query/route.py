import os.path

from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import login_required, group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/')
def start_query():
    return render_template('menu_query.html')


@blueprint_query.route('/query1', methods=['GET', 'POST'])
def query_page1():
    if request.method == 'GET':
        return render_template('easy_request_1.html')
    else:
        input_city= request.form.get('city')

        if input_city:
            _sql = provider.get('easy_request_1.sql', input_city=input_city)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"


@blueprint_query.route('/query2', methods=['GET', 'POST'])
def query_page2():
    if request.method == 'GET':
        return render_template('easy_request_2.html')
    else:
        input_group = request.form.get('group')

        if input_group:
            _sql = provider.get('easy_request_2.sql', input_group=input_group)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"


@blueprint_query.route('/query3', methods=['GET', 'POST'])
def query_page3():
    if request.method == 'GET':
        return render_template('easy_request_3.html')
    else:
        input_name = request.form.get('name')

        if input_name:
            _sql = provider.get('easy_request_3.sql', input_name=input_name)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"


@blueprint_query.route('/query4', methods=['GET', 'POST'])
def query_page4():
    if request.method == 'GET':
        return render_template('easy_request_4.html')
    else:
        input_order = request.form.get('order')

        if input_order:
            _sql = provider.get('easy_request_4.sql', input_order=input_order)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"


@blueprint_query.route('/query5', methods=['GET', 'POST'])
def query_page5():
    if request.method == 'GET':
        return render_template('easy_request_5.html')
    else:
        input_year = request.form.get('year')

        if input_year:
            _sql = provider.get('easy_request_5.sql', input_year=input_year)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"


@blueprint_query.route('/query6', methods=['GET', 'POST'])
def query_page6():
    if request.method == 'GET':
        return render_template('easy_request_6.html')
    else:
        name = request.form.get('name')

        if name:
            _sql = provider.get('easy_request_6.sql', input_name=name)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"