from flask import request
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Redprint('client')

@api.route('/register', methods=['POST'])
def create_client():
    #注册和登录，最好提供统一的API接口
    #参数 校验 接收参数
    #WTForm 验证表单
    form = ClientForm().validate_for_api()
    #用字典的方式处理不同客户端的注册
    promise = {
            ClientTypeEnum.USER_EMAIL:__register_user_by_email
        }
    #键：枚举类型。 取值并执行
    promise[form.type.data]()
    return Success()
#总 分
#所有客户端都要携带的参数写在总
#各个客户端的特别属性卸载分
def __register_user_by_email():
    #request.json('nickname') 这样获取的数据没经过验证
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data,
                                form.account.data,
                                form. secret.data)
