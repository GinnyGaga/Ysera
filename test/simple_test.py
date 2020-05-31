# coding=utf-8

import datetime
import logging.config
import os
import time

# <editor-fold desc="日志系统">
# 日志输出路径
BASE_DIR = "/log/"


def get_now() -> str:
    """
    返回当前时间
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def log_file_name() -> str:
    """
    返回日志文件名
    """
    # 如果地址不存在，则自动创建log文件夹
    prefix = os.getcwd()
    path = prefix + BASE_DIR
    if os.path.exists(path) is False:
        os.mkdir(path)
    # return "loop_check_{}.log".format(get_now())
    return os.path.join(path, "loop_check_{}.log".format(get_now()))


# 日志配置项
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s][%(asctime)s]%(message)s'  # 日志输出格式
        },
        'standard': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'  # 日志输出格式
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',  # 控制台日志输出级别
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',  # 文件日志输出级别
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file_name(),
            'maxBytes': 1024 * 1024 * 50,  # 文件分割大小
            'backupCount': 10,  # 日志备份文件数
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


# </editor-fold desc="日志系统">


# <editor-fold desc="命令采集业务逻辑">
class CmdBase(object):
    """
    命令执行基类
    """

    def __init__(self, cmd: str):
        if cmd is None or len(cmd) == 0:
            raise Exception("cmd is empty")
        self.cmd = cmd

    def execute(self) -> str:
        """
        execute cmd
        """
        r = os.popen(self.cmd)
        text = r.read()
        r.close()
        return text


class GetProcessIds:
    """
    获取进程id类
    """

    def __init__(self):
        self._pnames_dict = {}

    def get_pnames_dict(self, p_names):
        for p_name in p_names:
            cmd = "ps -ef | grep {} | grep -v grep | awk '{{print$2,$8}}'".format(p_name)
            text = CmdBase(cmd).execute()
            logger.debug("\ncmd: {}\nresult: \n{}".format(cmd, text))

            if len(text) == 0:
                self._pnames_dict[p_name] = []
            else:
                # """
                # Example:
                # 22707 nginx:\n
                # 23876 nginx:\n
                # 30467 /home/webserver\n
                # """
                line = text.split("\n")
                p_ids = []
                for info in line:
                    if len(info) == 0:
                        continue
                    p_ids.append(info.split(" ")[0])
                self._pnames_dict[p_name] = p_ids

        return self._pnames_dict


class GetProcessOpenFdsCount(CmdBase):
    """
    获取进程打开文件数类
    """
    _pids_dict = {}
    _pnames_pids_dict = {}  # [pname]([pid]count)

    def __init__(self, pname_dict: dict):
        sub_cmd = self._get_sub_cmd(pname_dict)
        cmd = "lsof -n | awk '{{print $2}}' | sort | uniq -c | grep -E '{}'".format(sub_cmd)
        super(GetProcessOpenFdsCount, self).__init__(cmd)

    def _get_sub_cmd(self, pname_dict):
        if pname_dict is None or len(pname_dict) == 0:
            raise Exception("pname_dict is None or empty")
        tmp_pids = []
        for pname, pids in pname_dict.items():
            self._pnames_pids_dict[pname] = {}
            for pid in pids:
                self._pids_dict[pid] = pname
                tmp_pids.append(pid)
        return "|".join(tmp_pids)

    def get_open_fds_count(self):
        text = self.execute()
        if len(text) == 0:
            return
        # """
        # 40 22707
        # 27 23876
        # 136 30467
        # """
        logger.debug("\ncmd: {}\nresult: \n{}".format(self.cmd, text))

        line = text.split("\n")
        for info in line:
            if len(info) == 0:
                continue
            data_list = info.strip().split(" ")
            count = data_list[0]
            pid = data_list[1]
            pname = self._pids_dict[pid]
            sub_pids_dict = self._pnames_pids_dict[pname]
            sub_pids_dict[pid] = count

        return self._pnames_pids_dict  # [pname]([pid](open_fds_count))


# </editor-fold desc="命令采集业务逻辑">


# <editor-fold desc="任务系统">
class TaskBase(object):
    def __init__(self, name: str, cmder: CmdBase):
        self.name = name
        self.cmder = cmder

    def do(self):
        self.print(self.cmder.execute())

    def print(self, info):
        logger.info("\n"
                    "task_name: {}\n"
                    "result:\n"
                    "{}\n".format(self.name, info))


class TaskGetProcessOpenFdsCount(TaskBase):
    def __init__(self, name: str, pnames: list):
        if pnames is None or len(pnames) == 0:
            raise Exception("pnames is empty")
        self.pnames = pnames
        super(TaskGetProcessOpenFdsCount, self).__init__(name, CmdBase("empty"))

    def do(self):
        pnames_dict = GetProcessIds().get_pnames_dict(self.pnames)
        open_fds_info = GetProcessOpenFdsCount(pnames_dict).get_open_fds_count()
        self.print(open_fds_info)


# </editor-fold desc="任务系统">


# <editor-fold desc="主函数">
# 执行间隔（s）
EXECUTION_INTERVAL = 60


def run():
    tasks = [
        TaskGetProcessOpenFdsCount("check_process_open_fds_count", ["nginx", "webserver"]),
        TaskBase("check_disk_usage", CmdBase("df -i")),
        TaskBase("check_signal", CmdBase("ipcs -a")),
    ]

    while True:
        for task in tasks:
            task.do()
        logger.info("The next check will be executed in {} seconds\n"
                    "============================================="
                    "=============================================".format(EXECUTION_INTERVAL))
        time.sleep(EXECUTION_INTERVAL)


if __name__ == '__main__':
    run()
# </editor-fold desc="主函数">
