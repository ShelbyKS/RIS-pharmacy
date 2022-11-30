import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBConnection
from db_work import select_dict
from sql_provider import SQLProvider

blueprint_edit = Blueprint('bp_edit', __name__, template_folder="templates")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_edit.route('/', methods=['GET'])
def show_all_products():
    db_config = current_app.config['db_config']
    _sql = provider.get('all_products.sql')
    products = select_dict(db_config, _sql)
    return render_template('all_products.html', products=products)


@blueprint_edit.route('/', methods=['POST'])
def check_product():
    db_config = current_app.config['db_config']
    action = request.form.get('action')
    med_id = request.form.get('prod_id')
    print("prod_id = ", med_id)
    print("action = ", action)
    if action == 'edit_prod':
        _sql = provider.get('get_product_by_id.sql', prod_id=med_id)
        product = select_dict(current_app.config['db_config'], _sql)
        print("product=", product)
        return render_template('product_update.html', product=product)
    if action == 'del_prod':
        with DBConnection(db_config) as cursor:
            if cursor is None:
                raise ValueError('Курсор не создан')
            _sql = provider.get('delete_product.sql', prod_id=med_id)
            result1 = cursor.execute(_sql)
            if result1:
                return "Товар удалён"
            else:
                return "Что-то пошло не так"


@blueprint_edit.route('/edit', methods=['POST'])
def edit_product():
    if request.method == 'POST':
        db_config = current_app.config['db_config']
        prod_price = request.form.get('prod_price')
        prod_amount = request.form.get('prod_amount')
        prod_id = request.form.get('id_med')
        print(prod_id, prod_price, prod_amount)
        return "Что-то пошло не так"

        '''
        if prod_price and prod_amount:
            with DBConnection(db_config) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')
                _sql = provider.get('update_product.sql', prod_price=prod_price, prod_amount=prod_amount, prod_id=prod_id)
                result1 = cursor.execute(_sql)
                if result1:
                    return "Товар обновлен"
                else:
                    return "Что-то пошло не так"
        else:
            return "Repeat input"

@blueprint_edit.route('/insert_prod', methods=['GET'])
def insert_prod():
    product={}
    return render_template('product_update.html', product=product)


@blueprint_edit.route('/insert_prod', methods=['POST'])
def inserted_prod():
    message = 'Товар добавлен в бд'
    return render_template('update_ok.html', message=message)

'''

