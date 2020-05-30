# coding=utf-8

TASK_LIST = [{
    "task": "test_get_pids",
    "cron": 10,
    "class": "RecordProcessOpenFdsCount",
    "detail": {
        "pNames": [
            "nginx",
            "webserver",
        ],
    }
}]
