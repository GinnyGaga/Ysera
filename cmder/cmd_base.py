# coding=utf-8
import os

from common.excep import ErrorInvalidParameter
from common.log import logger


class CmdBase(object):
    """
    Record the command to be executed
    """

    def __init__(self, cmd: str):
        if self.cmd is None or len(self.cmd) == 0:
            raise ErrorInvalidParameter(ex="cmd is empty")
        self.cmd = cmd

    def execute(self) -> str:
        """
        execute cmd
        """
        logger.debug("cmd: {}".format(self.cmd))
        r = os.popen(self.cmd)
        text = r.read()
        r.close()
        return text


class CheckProcessExists(CmdBase):
    def __init__(self, p_name):
        if p_name is None or len(p_name) == 0:
            raise ErrorInvalidParameter(ex="process name is empty")
        cmd = "ps -ef | grep {}".format(p_name)
        super(CheckProcessExists, self).__init__(cmd)


class GetProcessIds(CmdBase):
    pids_dict = {}

    def __init__(self, p_names: list):
        sub_cmd = "|".join(p_names)
        cmd = "ps -ef | grep -E '{}' | grep -v grep | awk '{{print$2,$8}}'".format(sub_cmd)
        super(GetProcessIds, self).__init__(cmd)

        for name in p_names:
            self.pids_dict[name] = None

    def get_pid_dict(self):
        text = self.execute()
        logger.info("\ncmd: {}\nresult: \n{}".format(self.cmd, text))


class GetProcessIdsV2:
    def __init__(self):
        self._pnames_dict = {}

    def get_pnames_dict(self, p_names):
        for p_name in p_names:
            cmd = "ps -ef | grep {} | grep -v grep | awk '{{print$2,$8}}'".format(p_name)
            text = CmdBase(cmd).execute()
            logger.info("\ncmd: {}\nresult: \n{}".format(cmd, text))

            if len(text) == 0:
                self._pnames_dict[p_name] = []
            else:
                # """
                # Example:
                # 22707 nginx:\n
                # 23876 nginx:\n
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
    _pids_dict = {}
    _pnames_pids_dict = {}  # [pname]([pid]count)

    def __init__(self, pname_dict: dict):
        if pname_dict is None:
            raise ErrorInvalidParameter(ex="pname_dict is None.")
        tmp_pids = []
        for pname, pids in pname_dict.items():
            self._pnames_pids_dict[pname] = {}
            for pid in pids:
                self._pids_dict[pid] = pname
                tmp_pids.append(pid)
        sub_cmd = "|".join(tmp_pids)
        cmd = "lsof -n | awk '{{print $2}}' | sort | uniq -c | grep -E '{}'".format(sub_cmd)
        super(GetProcessOpenFdsCount, self).__init__(cmd)

    def get_open_fds_count(self):
        text = self.execute()
        if len(text) == 0:
            return
        # """
        # 40 22707
        # 27 23876
        # 136 30467
        # """
        logger.info("\ncmd: {}\nresult: \n{}".format(self.cmd, text))

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

        return self._pnames_pids_dict
