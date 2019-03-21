from app.libs.error import APIException

class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0

class DeleteSuccess(Success):
    code = 202
    #删除成功
    error_code = 1

class ServerError(APIException):
    code = 500
    msg = 'sorry, we make a mistake ^(*￣(oo)￣)^'
    error_code = 999

class ClientTypeError(APIException):
    #400参数错误，401未授权，403禁止访问，404没有找到资源或页面
    #500服务器未知错误
    #2开头，请求成功，200查询成功，201创建或更新成功，204删除成功
    #3重定向
    code = 400
    msg =  'client is invalid'
    error_code = 1006

class ParameterException(APIException):
    code = 400
    msg = 'validate parameter'
    error_code = 1000

class NotFound(APIException):
    code = 404
    msg = 'the resource are not_found 0__0!'
    error_code = 1001

class AuthFailed(APIException):
    code = 401  #授权失败
    msg = 'authorization failed'
    error_code = 1005

class Forbidden(AuthFailed):
    code = 403   #禁止访问，权限不够
    error_code = 1004
    msg = 'foebidden, not in scope'

class DuplicateGift(AuthFailed):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'