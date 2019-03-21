from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.error_code import ServerError


class JSONEncoder(_JSONEncoder):
    #Python遇到了不能序列化的对象都会调用default函数
    #添加更多的if处理
    def default(self, o):  #递归调用
        #判断对象o是否有keys属性和'__getitem__方法
        #hasattr判断是否存在
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        #Isinstance判断是否属于某种类型
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        #服务器出错，不必要知道具体的错误
        raise ServerError()

class Flask(_Flask):
    json_encoder = JSONEncoder

