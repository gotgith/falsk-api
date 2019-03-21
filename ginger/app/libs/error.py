from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999

    #实例化时 没有传参数，取默认值
    def __init__(self, msg=None, code=None, error_code=None,
                 headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        #调用HTTP..这个基类的构造函数
        #HTTP..会根据code和desciption自动生成response
        super(APIException, self).__init__(msg, None)
    #参考HTTP...中的get_body
    def get_body(self,  environ=None):
        body = dict(
            msg= self.msg,
            error_code = self.error_code,
            #让客户端知道当前的错误信是访问服务期的那个接口产生的异常
            request=request.method + ' ' + self.get_url_no_param()
        )
        #字典返回文本
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    #路径不包括主机名和端口号，也不包括？后前的参数
    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
