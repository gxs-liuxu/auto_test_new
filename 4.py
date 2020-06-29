from public.common.date import *
from public.interface.interface_class import *
from public.interface.parameter_change import parameter_change

def add(num):
    return num + 1


a = 'afafafsdf' + '123123' + str(add(10))
b = '123456' + str(add(10))
c = '123456 + add(10)'
#d = '{"detail":"呵呵呵328呵呵","duration":0,"height":0,"is_stick":0,"nickname":"|nickname|","portrait":"|portrait|' + get_millisecond_timestamp() + '" ,"rotation":0,"type":0,"width":0}'
d = '{"detail":"你好aaa111aaa！","duration":0,"height":0,"is_stick":0,"nickname":\'八零一\',"portrait":\'http://static.guxiansheng.cn/avatar/1332505512.jpg\' + parameter_change.get_millisecond_timestamp() + \',"rotation":0,"type":0,"width":0}'
e = 'parameter_change.get_millisecond_timestamp()'
f = '{"detail":"你好aaa111aaa！","duration":0,"height":0,"is_stick":0,"nickname":\'八零一\',"portrait":\'http://static.guxiansheng.cn/avatar/1332505512.jpg\' + \'?\' + parameter_change.get_millisecond_timestamp()  ,"rotation":0,"type":0,"width":0}'
g = '{"detail":"你好aaa111aaa！","duration":0,"height":0,"is_stick":0,"nickname":\'八零一\',"portrait":\'http://static.guxiansheng.cn/avatar/1332505512.jpg\' + \'?\'  + parameter_change.get_millisecond_timestamp() ,"rotation":0,"type":0,"width":0}'
h = '{"detail":"你好aaa111aaa！","duration":0,"height":0,"is_stick":0,"nickname":\'八零一\',"portrait":\'http://static.guxiansheng.cn/avatar/1332505512.jpg\' + \'?\' + parameter_change.get_millisecond_timestamp()  ,"rotation":0,"type":0,"width":0}'
print(eval(b + str(c)))
print(eval(h))

# a = '|abc|'
# print(a[0],a[-1])

i = str({"detail":"呵呵呵328呵呵","duration":0,"height":0,"is_stick":0,"nickname":'什么鬼啊',"portrait":'123123.jpg'+ '?' + parameter_change.get_millisecond_timestamp()  ,"rotation":0,"type":0,"width":0})
print(eval(i))