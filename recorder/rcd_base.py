# coding=utf-8
from cmder.cmd_base import GetProcessIdsV2, GetProcessOpenFdsCount
from common.log import logger


class RecorderBase(object):
    def __init__(self, task_detail: dict):
        self.detail = task_detail

    def do(self):
        """
        Please override this function. It will be called after dynamically creating the class instance.
        """
        return


class RecordProcessId(RecorderBase):
    def __init__(self, task_detail: dict):
        super(RecordProcessId, self).__init__(task_detail)

    def do(self):
        logger.debug(self.detail)
        p_names = self.detail["pNames"]
        pnames_dict = GetProcessIdsV2().get_pnames_dict(p_names)
        logger.info("pids_dict: {}".format(pnames_dict))


class RecordProcessOpenFdsCount(RecorderBase):
    def __init__(self, task_detail: dict):
        super(RecordProcessOpenFdsCount, self).__init__(task_detail)

    def do(self):
        logger.debug(self.detail)
        p_names = self.detail["pNames"]
        pnames_dict = GetProcessIdsV2().get_pnames_dict(p_names)
        logger.info("pids_dict: {}".format(pnames_dict))
        # pnames_dict = {'nginx': ['22707', '23876'], 'webserver': ['30467']}
        open_fds_info = GetProcessOpenFdsCount(pnames_dict).get_open_fds_count()
        logger.info("open_fds_info: {}".format(open_fds_info))
