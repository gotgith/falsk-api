
class Scope:
    allow_api = []
    allow_module = []
    #排除普通用户个别不能访问的视图函数
    forbidden = []
    #运算符重载
    #可以使用+号代替add
    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        #利用集合（set）数据结构不能重复的特性，去重
        self.allow_api = list(set(self.allow_api))
        #返回self，就可以使用链式add了

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))
        return self

class AdminScope(Scope):
    #记录可以访问的视图函数
    #因为视图函数注册在蓝图上，而不是核心对象app，所有要加v1.
    # allow_api = ['v1.user+super+get_user',
    #              'v1.user+super_delete_user']
    allow_module = ['v1.user']
    def __init__(self):
        # self + UserScope()
        print(self.allow_api)

class UserScope(Scope): #根据需要添加视图函数
    #allow_api = ['v1.user+get_user', 'v1.user+delete_user']
    #排除
    forbidden = ['v1.user+super+get_user',
                  'v1.user+super_delete_user']
    def __init__(self):
        self + AdminScope()

# #只需关注特定的视图函数
# class SuperScope(Scope):
#     allow_api = ['v1.C', 'v1.D']
#     allow_module = ['v1.user']
#
#     def __init__(self):
#         #链式add,添加视图函数
#         #使用内置add，完成符号相加
#         self + UserScope() + AdminScope()
#         print(self.allow_api)

#根据scope查看endpoint是否在AdminScope和UserScope类下面的allow_api中
def is_in_scope(scope, endpoint):
    #通过一个类的名字得到这个类的对象用globals
    #globals可以把当前模块下面的所有的变量（包括类）变成一个字典
    #调式后发现globals是一个字典，键是scope，拿到的值是一个class，可实例化
    #endpoint:v1.view_func改为v1.red_name+view_func
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    #排除
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False