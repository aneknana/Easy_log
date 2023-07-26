''' logger '''
import logging
import sys
import time
from os import path
from typing import Callable
from functools import partial

def retry_fun(attempts_num: int) -> Callable:
    ''' get number of tries '''
    total_attempts = attempts_num
    def call_function(func: Callable) -> Callable:
        ''' get function '''
        def func_call(*args, **kwargs) -> None:
            ''' run function '''
            nonlocal  attempts_num
            while attempts_num > 0:
                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        return result
                    break
                except Exception as ex:
                    attempts_num -= 1
                    if attempts_num == 0:
                        ex.args = tuple(f'attempts_num = {total_attempts} : ' * (_==0) + ex.args[_] for _ in range(len(ex.args)))
                        raise ex
        func_call.repr_name = func.__name__
        return func_call
    return call_function

def timer_fun(func: Callable) -> Callable:
    ''' set timer '''
    def __str_time(c_time):
        return time.strftime("%Y-%m-%d %H:%M:%S", c_time)
    def func_call(*args, **kwargs) -> None:
        ''' run function '''
        time_start = time.localtime()
        if 'repr_name' not in dir(func):
            func.repr_name = func.__name__
        try:
            result = func(*args, **kwargs)
            time_end = time.localtime()
            time_str = f'''Function {func.repr_name}:
started at:  {__str_time(time_start)}
finished at: {__str_time(time_end)}
time spent:  {time.strftime("%H:%M:%S", time.gmtime(time.mktime(time_end) - time.mktime(time_start)))}'''
            func_call.time_str = time_str
            if result is not None:
                return result
        except Exception as ex:
            time_end = time.localtime()
            time_str = f'''Function {func.repr_name}:
started at:  {__str_time(time_start)}
error at: {__str_time(time_end)}
time spent:  {time.strftime("%H:%M:%S", time.gmtime(time.mktime(time_end) - time.mktime(time_start)))}'''
            func_call.time_str = time_str
            raise ex
    func_call.repr_name = func.__name__
    return func_call

def __get_logger__(console_level: int = 10, file_level: int = 10, name: str = 'log', file_path: str = 'log.log') -> Callable:
    ''' return custom logger object levels to choose:
        {'NOTSET': 0, 'DEBUG': 10, 'INFO': 20, 'WARN': 30, 'ERROR': 40, 'CRITICAL': 50} '''
    logg = logging.getLogger(name)
    logg.setLevel(level=10)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    while logg.hasHandlers():
        logg.removeHandler(logg.handlers[0])
    if console_level in (10, 20, 30, 40, 50):
        c_handler = logging.StreamHandler()
        c_handler.setLevel(level = console_level)
        c_handler.setFormatter(formatter)
        logg.addHandler(c_handler)
    if file_level in (10, 20, 30, 40, 50):
        f_handler = logging.FileHandler(file_path, 'a', encoding = 'utf-8')
        f_handler.setLevel(level = file_level)
        f_handler.setFormatter(formatter)
        logg.addHandler(f_handler)
    return logg

def __args_to_str__(*args):
    ''' return string to print arguments list '''
    return f'Arguments: {", ".join(map(str, args))}' if len(args) > 0 else ''

def __kwargs_to_str__(**kwargs):
    ''' return string to print key value arguments list '''
    return f'Key value arguments: {", ".join([x + ": " + (str(y)[:75] + "..") if len(str(y)) > 75 else str(y) for x, y in kwargs.items()])}' if len(kwargs) > 0 else ''

def __add_print_fun__(new_print_fun: Callable) -> Callable:
    def decorator(old_print_fun: Callable) -> Callable:
        def inner_call(*args, **kwargs):
            old_print_fun(*args, **kwargs)
            new_print_fun(*args, **kwargs)
        return inner_call
    return decorator

def __log__(func: Callable, fun_logger: logging.Logger) -> Callable:
    ''' get function '''
    def func_call(*args, **kwargs):
        ''' run function '''
        nonlocal fun_logger
        if 'repr_name' not in dir(func):
            func.repr_name = func.__name__
        fun_logger.debug(f'''Function {func.repr_name} started. {", ".join(filter(None, (__args_to_str__(*args), __kwargs_to_str__(**kwargs))))}''')
        try:
            result = func(*args, **kwargs)
            if 'time_str' in dir(func):
                func_call.time_str = func.time_str
            fun_logger.debug(f'Function {func.repr_name} ended')
            if result is not None:
                return result
        except Exception as ex:
            if 'time_str' in dir(func):
                func_call.time_str = func.time_str
            fun_logger.error(f'Error on function {func.repr_name} call: {str(ex)}')
    return func_call

def log_cls(cls, **kwargs) -> Callable:
    'applies log decorator to all class methods that not start from _'
    if 'c_logger' not in kwargs:
        c_logger = __get_logger__(name = path.basename(sys._getframe(1).f_code.co_filename),
                                  file_path = path.join(path.dirname(sys._getframe(1).f_code.co_filename), 'log.log'))
    else:
        c_logger = kwargs['c_logger']
    for method in dir(cls):
        if method == 'log_function':
            for loger_fun in ['error', 'fatal']:
                setattr(c_logger, loger_fun, __add_print_fun__(getattr(cls, method))(getattr(c_logger, loger_fun)))
    for method in dir(cls):
        if method[0] != '_' and callable(getattr(cls, method)) and method != 'log_function':
            setattr(cls, method, __log__(getattr(cls, method), c_logger))
    return cls

def log_fun(func, **kwargs) -> Callable:
    'applies log decorator to function'
    if 'c_logger' not in kwargs:
        c_logger = __get_logger__(name = path.basename(sys._getframe(1).f_code.co_filename),
                                  file_path = path.join(path.dirname(sys._getframe(1).f_code.co_filename), 'log.log'))
    else:
        c_logger = kwargs['c_logger']
    return __log__(func, c_logger)

def log_cls_custom(console_level: int = 10, file_level: int = 10, name: str = None, file_path: str = None) -> Callable:
    ''' gets information about logger '''
    i_logger = __get_logger__(console_level, file_level,
                              name = name if name is not None else path.basename(sys._getframe(1).f_code.co_filename),
                              file_path = file_path if file_path is not None else path.join(path.dirname(sys._getframe(1).f_code.co_filename), 'log.log'))
    return partial(log_cls, c_logger = i_logger)

def log_fun_custom(console_level: int = 10, file_level: int = 10, name: str = None, file_path: str = None) -> Callable:
    ''' gets information about logger '''
    i_logger = __get_logger__(console_level, file_level,
                              name = name if name is not None else path.basename(sys._getframe(1).f_code.co_filename),
                              file_path = file_path if file_path is not None else path.join(path.dirname(sys._getframe(1).f_code.co_filename), 'log.log'))
    return partial(log_fun, c_logger = i_logger)