** Ysera是一个辅助记录系统稳定性测试数据的工具 **
- 依赖
	python3.x

- 未完待续
	1.cron设置级别定时任务
	2.excel写入
	3.性能上报
	
- 使用
	1.继承CmdBase及RecorderBase类编写自己的观测业务逻辑
	2.修改tasks_conf文件
```
TASK_LIST = [{
    "task": "Check任务名称",
    "cron": 10,
    "class": "你所编写的RecordClass名称",
    "detail": "任务中的所需参数，需要是json格式"
    }
}]
```
3.将....\Ysera设置为python工作目录
4.执行\test\run.py

- 注意
配置中每一个task都将在一个独立的线程中执行，请尽量将可并行的check放置在同一个task中
