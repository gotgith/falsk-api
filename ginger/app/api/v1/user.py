from flask import jsonify, g
from app.libs.error_code import DeleteSuccess, AuthFailed
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

api = Redprint('user')

#管理员查询接口
@api.route('/<int:uid>', methods=['GET'])
#接口保护，确认用户身份
@auth.login_required
def super_get_user(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    # dict, 笨方法
    # r = {
    #     'nickname':user.nickname,
    #     'email':user.email
    # }
    # return jsonify(r)
    return jsonify(user)

#普通用户查询接口
@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)

#管理员删除
@api.route('/<int:uid>', methods=['DELETE'])
def super_delete_user(uid):
    pass

#删除用户
@api.route('', methods=['DELETE'])
#接口保护，确认用户数身份
@auth.login_required
def delete_user():
    #使用token中的用户信息，避免超权操作
    uid = g.user.uid
    #g变量是线程隔离的，不会发生多用户情况的id错乱现象
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()