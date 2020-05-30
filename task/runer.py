# coding=utf-8
from common.excep import MyException, ErrorDuplicateTask
from conf.tasks_conf import TASK_LIST
from common.log import logger
from task.task import TaskHelper


class RunnerBase(object):
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        t_list = TASK_LIST
        tasks_name_dict = {}

        for t in t_list:
            task_name = t["task"]
            if task_name in tasks_name_dict:
                raise ErrorDuplicateTask({"task_name: {}".format(task_name)})
            tasks_name_dict[task_name] = None

            self.tasks.append(TaskHelper.build_task(t))

    def new_class(self, cname, task_detail):
        return getattr(__import__("recorder.rcd_base", fromlist=["rcd_base"]), cname)(task_detail)


class Runner(RunnerBase):
    def __init__(self):
        try:
            super(Runner, self).__init__()
            if len(self.tasks) == 0:
                return
            for task in self.tasks:
                logger.debug("task.info: [{}]-[{}]-[{}]-[{}]".format(task.name, task.cron, task.cname, task.detail))
                inst = self.new_class(task.cname, task.detail)
                inst.do()
        except MyException as e:
            logger.error("code: {}, desc: {}, ex: {}".format(e.code(), e.desc(), e.ex))
        except Exception as e:
            logger.exception(e)
            logger.error("Exception err: {}".format(e))
