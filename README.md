# easy_log

decorates functions and public class methods
simply writes to log file time of start and end and errors

timer_fun creates time_str attribute to function that can be used later

example
@easy_log.log_cls
class MyClass():
    @easy_log.timer_fun
    @easy_log.retry_fun(3)
    def __call__(self):
        self.task1()
        self.task2()
    def self.task1(self) -> None:
        pass
    def self.task2(self) -> None:
        pass

obj = MyClass()
obj()
print(obj.__call__.time_str)