from flask import Blueprint
from app.api.v1 import book, user, client, token, gift


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    #实现注册register，接收一个蓝图参数，就把红图注册到了蓝图上了
    book.api.register(bp_v1)
    user.api.register(bp_v1)
    client.api.register((bp_v1))
    token.api.register(bp_v1)
    gift.api.register(bp_v1)
    return bp_v1

