
class Redprint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        #模仿蓝图
        # f是使用装饰器的定义的函数名
        def decorator(f):#实现视图函数向蓝图函数的注册
            #不能直接拿到蓝图对象，先把信息保存起来，后期总会碰到蓝图对象
            self.mound.append((f, rule, options))
            return f
        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound: #序列解包
            #options是字典，字典pop：去到某一个值并把原来字典的值删除
            #f.__name__取默认值，因options中不一定有以endpoint为建的值
            #意思就是option里有endpoint就直接取到endpoint的值，
            # 如果没有就取视图函数的名字作为endpoint的值
            #把endpoint改成红图和视图函数的名字
            endpoint = self.name + '+' + options.pop('endpoint', f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)

