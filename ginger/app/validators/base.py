from flask import request
from wtforms import Form
from app.libs.error_code import ParameterException

class BaseForm(Form):
    def __init__(self):
        #silent静默，不要报错
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        #调用了validate之后所有的错误异常信息都存在form中的error中
        #可以分类处理异常
        if not valid:
            raise ParameterException(msg=self.errors)
        return self

