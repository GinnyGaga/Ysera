# coding=utf-8
import threading
import time

from common.excep import ErrorInvalidConf


class Task(threading.Thread):
    def __init__(self, name: str, cron: int, cname, detail: dict):
        threading.Thread.__init__(self)

        self.name = name
        self.cron = cron
        self.cname = cname
        self.detail = detail

    def new_class(self, cname, task_detail):
        return getattr(__import__("recorder.rcd_base", fromlist=["rcd_base"]), cname)(task_detail)

    def run(self) -> None:
        while True:
            inst = self.new_class(self.cname, self.detail)
            inst.do()
            time.sleep(self.cron)


class TaskHelper:
    @staticmethod
    def build_task(task: dict):
        try:
            return Task(task["task"], task["cron"], task["class"], task["detail"])
        except KeyError as e:
            raise ErrorInvalidConf(ex=e.__str__())
