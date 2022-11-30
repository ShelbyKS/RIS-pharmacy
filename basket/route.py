import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBConnection
from db_work import select_dict, insert
from sql_provider import SQLProvider
from cache.wrapper import fetch_from_cache, update_cache
from datetime import datetime

blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


items = 1

@blueprint_order.route('/', methods=['GET','POST'])
def order_index():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']
    cached_select = fetch_from_cache('all_items_cached', cache_config)(select_dict) #явное задание декоратора
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = cached_select(db_config, sql)
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket=basket_items)
    else:
        prod_id = request.form['id_med']
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)

        add_to_basket(prod_id, items)

        return redirect(url_for('bp_order.order_index'))


def add_to_basket(prod_id: str, items: dict):
    item_description = [item for item in items if str(item['id_med']) == str(prod_id)]
    print('item_description before=', item_description)
    item_description = item_description[0]
    curr_basket = session.get('basket', {})

    if prod_id in curr_basket:
        if curr_basket[prod_id]['amount'] < item_description['med_amount']:
            curr_basket[prod_id]['amount'] = curr_basket[prod_id]['amount'] + 1
    else:
        curr_basket[prod_id] = {
            'med_name': item_description['med_name'],
            'med_price': item_description['med_price'],
            'med_amount': item_description['med_amount'],
            'amount': 1
        }
        session['basket'] = curr_basket
        session.permanent = True
    return True


@blueprint_order.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_order.order_index'))


@blueprint_order.route('/save_order', methods=['GET', 'POST'])
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {})
    cache_config = current_app.config['cache_config']
    db_config = current_app.config['db_config']

    order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket)
    if order_id:
        session.pop('basket', {})
        sql = provider.get('all_items.sql')
        cached_select_update = update_cache('all_items_cached', cache_config)(select_dict)  # явное задание декоратора
        items = cached_select_update(db_config, sql)

        return render_template('order_created.html', order_id=order_id)
    else:
        return 'Что-то пошло не так :('


def save_order_with_list(dbconfig:dict, user_id:int, current_basket:dict):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        _sql1 = provider.get('insert_order.sql', user_id=user_id, order_date=datetime.now())
        result1 = cursor.execute(_sql1)
        if result1 == 1:
            _sql2 = provider.get('select_order_id.sql', user_id=user_id)
            cursor.execute(_sql2)
            order_id = cursor.fetchall()[0][0]
            print('order_id=', order_id)
            if order_id:
                for key in current_basket:
                    print(key, current_basket[key]['amount'])
                    prod_amount = current_basket[key]['amount']
                    _sql3 = provider.get('insert_order_list.sql', order_id=order_id, prod_id=key, prod_amount=prod_amount)
                    cursor.execute(_sql3)
                return order_id
