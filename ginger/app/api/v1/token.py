from flask import current_app, jsonify
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm
#生成令牌的库
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,\
    BadSignature, SignatureExpired

api = Redprint('token')

#登录
@api.route('', methods=['POST'])
def get_token():
    #格式验证
    form = ClientForm().validate_for_api()
    #正确性验证
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identify = promise[ClientTypeEnum(form.type.data)](
        form.account.data, form.secret.data)
    #过期时间，写入配置文件中
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identify['uid'],
                                form.type.data,
                                identify['scope'],
                                expiration)
    #此时返回的token是base加密类型的字符串，需要转为普通的字符串decode
    # 需要返回json格式
    t = {
        'token':token.decode('ascii')
    }
    #序列化
    return jsonify(t), 201

#令牌过期验证
@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    return jsonify(r)

#生成token
#ac_type 客户端类型
#expiration 有效时间
def  generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    #把信息以字典的形式写入到令牌中，返回的是字符串（token令牌）
    return s.dumps({
        'uid':uid,
        'type':ac_type.value,
        'scope':scope
    })
