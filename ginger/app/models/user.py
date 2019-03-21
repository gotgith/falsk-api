from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db

class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(20), unique=True)
    #权限标识，默认值为1是普通用户，2为管理员
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    def keys(self):
        return ['nickname', 'id', 'email', 'auth']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password= generate_password_hash(raw)

    #在一个对象下面创建对象对象本身，从面对对象的角度是不合理的
    #如果视作静态方法或者类方法，那个逻辑就是合理的
    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)
    @staticmethod
    def verify(email, password):
        #数据库查询用户是否存在
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth==2 else 'UserScope'
        return {'uid':user.id, 'scope':scope}

    #把原始密码加密后，再进行密码验证
    def check_password(self,raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

