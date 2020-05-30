# coding=utf-8

TASK_LIST = [{
    "task": "test_get_pids",
    "cron": 5,
    "class": "RecordProcessOpenFdsCount",
    "detail": {
        "pNames": [
            "nginx",
            "webserver",
        ],
    }
}]
