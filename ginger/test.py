
class JH(object):
    name = 'lala'
    age = 18

    def __init__(self):
        self.gender = 'male'

    def keys(self):
        return ('name', 'age', 'gender')
        #元组只有单个元素，要在这个元素后面加逗号
        #return ('name',)
        #省去上面的麻烦,使用列表
        #return ['name']

    #可以使对象以[]的形式访问
    def __getitem__(self, item):
        #通过对象下面的属性的名字拿到这个属性的值
        return getattr(self, item)
o = JH()
print(dict(o)) #拿到字典
#使用__getitem__可以访问到值，把name当作item参数传递
# 方法返回的值就是o[]调用的结果
print(o['name'])#拿到对应的值
print(o['age'])

#只能拿到实例变量，不能拿到类变量
#JH().__dict__
#o = JH()
#调用dict方法时传递了一个对象，Python会去调用这个对象下面的keys方法
#调用keys目的就是拿到所有这个字典的键，键是由我们自己定义
#dict(o)


