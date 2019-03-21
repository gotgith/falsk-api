from http.client import HTTPException
from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()

#捕捉所有异常.HTTPException,APIException,Exception
@app.errorhandler(Exception)
def framework_error(e):
    #isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。
    #type() 不会认为子类是一种父类类型，不考虑继承关系。
    #isinstance() 会认为子类是一种父类类型，考虑继承关系。
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        #log 用日记记录错误类型
        #开发过程中，也就是调试模式，需要具体的错误
        #上线后或向前端提供数据服务，调式模式关闭，提供简单的错误提示
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e

#判断当前文件是否是入口文件
if __name__ == '__main__':
    #启动web服务器,打开调试模式
    app.run(debug=True)