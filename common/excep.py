# coding=utf-8
from common.error import ErrCode


class MyException(Exception):
    def __init__(self, code, desc, ex=None):
        self._code = code
        self._desc = desc
        if ex is not None:
            self._ex = {
                "info": ex
            }
        else:
            self.ex = {}

    def ex(self):
        return self._ex

    def code(self):
        return self._code

    def desc(self):
        return self._desc


class ErrorInvalidParameter(MyException):
    def __init__(self, ex=None):
        super(ErrorInvalidParameter, self).__init__(ErrCode.InvalidParams[0], ErrCode.InvalidParams[1], ex)


class ErrorInvalidConf(MyException):
    def __init__(self, ex=None):
        super(ErrorInvalidConf, self).__init__(ErrCode.InvalidConf[0], ErrCode.InvalidConf[1], ex)


class ErrorDuplicateTask(MyException):
    def __init__(self, ex=None):
        super(ErrorDuplicateTask, self).__init__(ErrCode.InvalidConf[0], ErrCode.InvalidConf[1], ex)
