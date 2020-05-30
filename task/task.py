# coding=utf-8
from common.excep import ErrorInvalidConf


class Task:
    def __init__(self, name: str, cron: str, cname, detail: dict):
        self.name = name
        self.cron = cron
        self.cname = cname
        self.detail = detail


class TaskHelper:
    @staticmethod
    def build_task(task: dict):
        try:
            return Task(task["task"], task["cron"], task["class"], task["detail"])
        except KeyError as e:
            raise ErrorInvalidConf(ex=e.__str__())

