from .app import Flask


def register_blueprint(app):
    from app.api.v1 import create_blueprint_v1
    #注册蓝图
    #加入参数url_prefix：加入红图的路径的前缀
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')

def register_plugin(app):
    from app.models.base import db
    db.init_app(app)  #插件注册
    #只有在app上下文环境中才能完成create_alla操作
    with app.app_context():#把app推入到上下文栈中
        db.create_all() #创建数据库的数据表


def create_app():
    app = Flask(__name__)
    #把配置文件装载到flask核心对象app中
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    register_blueprint(app)
    register_plugin(app)

    return app