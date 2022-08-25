import json
from flask import request
from config import app
import db_init
import classes


def get_put_delete_universal(request_method, cls_id, request_json, cls):
    """
    Общая функция для вывода методов get и post
    :param request_method: метод запроса
    :param cls_id: id по которому ищем изменяемый объект в базе
    :param request_json: данные для изменения
    :param cls: класс с который работаем
    :return: pp.response_class
    """
    if request_method == 'GET':
        return app.response_class(
            response=json.dumps(db_init.get_one(cls, cls_id), ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    elif request_method == 'PUT':
        return app.response_class(
            response=json.dumps(db_init.update_cls(cls, cls_id, request_json), ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    elif request_method == 'DELETE':
        return app.response_class(
            response=json.dumps(db_init.delete_cls(cls, cls_id), ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )

def get_post_universal(request_method, cls, request_json):
    """
    Общая функция для вывода методов get и post
    :param request_method: метод запроса
    :param cls: класс с который работаем
    :param request_json: данные если они есть
    :return: app.response_class
    """
    if request_method == 'GET':
        return app.response_class(
            response=json.dumps(db_init.get_all(cls), ensure_ascii=False),
            status=200,
            mimetype="application/json"
            )
    elif request_method == 'POST':
        if isinstance(request_json, list):
            db_init.insert_data(request_json, cls)
        elif isinstance(request_json, dict):
            db_init.insert_data([request_json], cls)

        return app.response_class(
                    response=json.dumps(request_json, ensure_ascii=False),
                    status=200,
                    mimetype="application/json")


@app.route("/users/", methods=['GET', 'POST'])
def get_all_users():
    return get_post_universal(request.method, classes.User, request.json)

@app.route("/users/<int:id>", methods=['GET', 'PUT', "DELETE"])
def get_user(id):
    return get_put_delete_universal(request.method, id, request.json , classes.User)


@app.route("/orders/", methods=['GET','POST'])
def get_all_orders():
    return get_post_universal(request.method, classes.Order, request.json)

@app.route("/orders/<int:id>", methods=['GET', 'PUT', "DELETE"])
def get_order(id):
    return get_put_delete_universal(request.method, id, request.json, classes.Order)

@app.route("/offers/", methods=['GET', 'POST'])
def get_all_offers():
    return get_post_universal(request.method, classes.User, request.json)

@app.route("/offers/<int:id>", methods=['GET', 'PUT', "DELETE"])
def get_offer(id):
    return get_put_delete_universal(request.method, id, request.json, classes.Offer)


if __name__ == '__main__':
    db_init.init_db()
    app.run()
