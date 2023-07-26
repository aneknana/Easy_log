import easy_log
import time
 
@easy_log.log_fun_custom(name = 'jjjjj')
@easy_log.timer_fun
@easy_log.retry_fun(2)
def myfunction(a, f):
    print(100/0)
    print((a+f) / 14)

@easy_log.log_fun
@easy_log.timer_fun
def myfunction2(a, f):
    return (a+f) / 14

myfunction(7, 10)
print(myfunction.time_str)
print(myfunction2(7, 15))
print(myfunction2.time_str)
myfunction(117, 10)

######################################
@easy_log.log_cls_custom()
class MyClass:
    a = 10
    b = 4
    def log_function(text):
        print('new_fun-------'+text)
    @easy_log.timer_fun
    @easy_log.retry_fun(3)
    def fun1(self):
        print(10/0)
    @easy_log.timer_fun
    def fun2(self):
        time.sleep(2)
        return self.a + self.b

a = MyClass()
a.fun1()
a.fun2()
print(a.fun2.time_str)
print(a.fun1.time_str)
