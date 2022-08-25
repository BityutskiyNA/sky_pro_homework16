import json

import classes
from config import db


def insert_data(data, cls):
    """
    Процедура загрузки данных в базу
    :param data: Данные которые грузим
    :param cls: класс в который грузим
    :return:
    """
    for row in data:
        db.session.add(cls(**row))

    db.session.commit()


def init_db():
    """
    Инициализируем базу данных, все записи удалятся из заново создаются
    :return:
    """
    db.drop_all()
    db.create_all()

    with open("data/user.json") as file:
        insert_data(json.load(file), classes.User)

    with open("data/orders.json") as file:
        insert_data(json.load(file), classes.Order)

    with open("data/offers.json") as file:
        insert_data(json.load(file), classes.Offer)


def get_all(cls):
    """
    Получить все данные из класса
    :param cls: класс из которого получаем данные
    :return: все данные которые есть в этой базе данных по указанному классу
    """
    result = []
    x = db.session.query(cls).all()
    for row in x:
        result.append(row.to_dict())
    return result


def get_one(cls, id):
    """
    Получаем конкретную запись из базы данных
    :param cls: класс из которого получаем данные
    :param id: идентификатор записи которую получаем
    :return:
    """
    result = db.session.query(cls).get(id)
    return result.to_dict()


def update_cls(cls, id, values):
    """
    Перезаписываем конкретную запись в базе данных
    :param cls: класс из которого обновляем данные
    :param id: идентификатор записи которую обновляем
    :param values: данные которые меняем в записи
    :return:
    """
    db.session.query(cls).filter(cls.id == id).update(values)
    db.session.commit()


def delete_cls(cls, id):
    """
    Процедура удаления конкретной записи в базе данных по указанному id
    :param cls: класс из которого удаляем данные
    :param id: идентификатор записи которую удаляем
    :return:
    """
    db.session.query(cls).filter(cls.id == id).delete()
    db.session.commit()
