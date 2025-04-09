# celery使用

```shell
# windows 环境下需要加 -P gevent
celery -A PostalSavings worker --loglevel=info -P gevent

```


我将为你提供一个完整的示例代码，展示如何在 Django 项目中使用 Celery 的 `app.conf.task_routes` 实现任务路由，将不同的任务分配到不同的队列中，并结合你的 Celery 配置。我们假设这是一个简单的 Django 项目 `PostalSavings`，包括两个任务（例如发送邮件和处理数据），并将其路由到不同的队列。

---







#### 3. 创建数据库
使用你的 MySQL 配置：


####  启动 Celery Worker
为不同队列启动不同的 Worker：
- 邮件队列 Worker：
  ```bash
  celery -A PostalSavings worker -Q email_queue -l info
  ```
- 数据队列 Worker：
  ```bash
  celery -A PostalSavings worker -Q data_queue -l info
  ```
或者用一个 Worker 处理所有队列：
```bash
celery -A PostalSavings worker -l info
```

#### 6. 测试任务
访问 http://localhost:8000/books/trigger/
，触发任务。你会看到：
- Worker 日志显示任务被分配到对应队列并执行。
- 浏览器返回任务 ID 和成功消息。



### 说明
1. **任务路由**：
   - `task_routes` 将 `send_email_task` 路由到 `email_queue`，`process_data_task` 路由到 `data_queue`。
   - 不同队列可以由独立的 Worker 处理，实现任务隔离。

2. **扩展性**：
   - 可以添加更多任务和队列，例如：
     ```python
     app.conf.task_routes.update({
         'myapp.tasks.high_priority_task': {'queue': 'priority_queue'}
     })
     ```

3. **调试**：
   - 使用 `debug_task` 检查任务上下文：`debug_task.delay()`。

# pycharm 设置

```shell

将PostalSavings设置为 源代码根目录
```

5. 启动 Celery Worker
   为不同队列启动不同的 Worker：

邮件队列 Worker：

```shell
celery -A PostalSavings worker -Q email_queue -l info
```

数据队列 Worker：

```bash
celery -A PostalSavings worker -Q data_queue -l info
```

或者用一个 Worker 处理所有队列：

```shell
celery -A PostalSavings worker -l info
```

使用celery multi

```text

sudo celery multi start 2 -A PostalSavings -Q:1 email_queue -Q:2 data_queue

celery multi stop 2 -A PostalSavings

pkill -9 -f "celery.*PostalSavings"
```

我来为你逐一解析 `sudo celery multi start 2 -A PostalSavings -Q:1 email_queue -Q:2 data_queue` 命令中每个参数的含义，帮助你理解这条命令的作用。

---

### 命令分解

```bash
sudo celery multi start 2 -A PostalSavings -Q:1 email_queue -Q:2 data_queue
```

#### `multi`

- **含义**：Celery 的子命令，用于管理多个 Worker 进程。
- **作用**：允许启动、停止或重启多个 Worker，而不是单个 Worker。它是生产环境中常用的工具，便于批量管理。

#### `start`

- **含义**：`multi` 的子命令，表示启动 Worker。
- **作用**：告诉 `celery multi` 要启动（而不是停止或重启）指定数量的 Worker 进程。
- **其他选项**：
    - `stop`：停止 Worker。
    - `restart`：重启 Worker。
    - `show`：显示 Worker 配置但不执行。

#### `2`

- **含义**：指定要启动的 Worker 数量。
- **作用**：这里表示启动 2 个独立的 Worker 进程，分别命名为 `celery1` 和 `celery2`（默认命名规则）。
- **示例**：如果改为 `3`，会启动 3 个 Worker（`celery1`, `celery2`, `celery3`）。

#### `-A PostalSavings`

- **含义**：`--app` 的缩写，指定 Celery 应用（Application）。
- **作用**：告诉 Celery 使用 `PostalSavings` 项目中的 Celery 实例（通常在 `PostalSavings/celery.py`
  中定义）。这里的 `PostalSavings` 是模块名，指向你的 Celery 配置。
- **例子**：如果你的 Celery 配置在 `myproject/celery.py`，可能是 `-A myproject`。

#### `-Q:1 email_queue`

- **含义**：
    - `-Q`：`--queues` 的缩写，指定 Worker 监听的队列。
    - `:1`：表示适用于第一个 Worker（`celery1`）。
    - `email_queue`：队列名称。
- **作用**：第一个 Worker（`celery1`）只处理 `email_queue` 中的任务。队列名必须与 `task_routes` 配置匹配。
- **例子**：如果任务路由中定义了 `'myapp.tasks.send_email_task': {'queue': 'email_queue'}`，则邮件任务会被路由到这个队列。

#### `-Q:2 data_queue`

- **含义**：
    - `-Q`：同上，指定队列。
    - `:2`：表示适用于第二个 Worker（`celery2`）。
    - `data_queue`：队列名称。
- **作用**：第二个 Worker（`celery2`）只处理 `data_queue` 中的任务。
- **例子**：如果任务路由中定义了 `'myapp.tasks.process_data_task': {'queue': 'data_queue'}`，则数据处理任务会被路由到这个队列。

---

### 整体作用

这条命令的完整含义是：

- 以超级用户权限启动 2 个 Celery Worker 进程。
- 使用 `PostalSavings` 项目中的 Celery 配置。
- 第一个 Worker（`celery1`）监听 `email_queue`，处理邮件相关任务。
- 第二个 Worker（`celery2`）监听 `data_queue`，处理数据相关任务。

---

### 输出解释

运行后输出：

```
celery multi v5.4.0 (opalescent)
> Starting nodes...
        > celery1@wangzedeMacBook-Air.local: OK
        > celery2@wangzedeMacBook-Air.local: OK
```

- `celery1@wangzedeMacBook-Air.local`：第一个 Worker 的名称和主机名。
- `celery2@wangzedeMacBook-Air.local`：第二个 Worker 的名称和主机名。
- `OK`：表示启动成功，Worker 已运行在后台。

---

### 参数扩展

这条命令还可以添加更多参数来增强功能：

- `--loglevel=info`：显示详细日志。
- `--logfile=/tmp/celery_%n.log`：将日志保存到文件（`%n` 表示 Worker 编号，如 `celery1`）。
- `--pidfile=/tmp/celery_%n.pid`：保存进程 ID 到文件，便于管理。
- `-c:1 2`：设置第一个 Worker 的并发数为 2。
- `-c:2 4`：设置第二个 Worker 的并发数为 4。

改进后的命令示例：

```bash
sudo celery multi start 2 -A PostalSavings \
    -Q:1 email_queue -c:1 2 \
    -Q:2 data_queue -c:2 4 \
    --loglevel=info \
    --logfile=/tmp/celery_%n.log \
    --pidfile=/tmp/celery_%n.pid
```

---

### 与代码的关联

你的 `celery.py` 中定义了：

```python
app.conf.task_routes = {
    'app01.tasks.send_email_task': {'queue': 'email_queue'},
    'app01.tasks.process_data_task': {'queue': 'data_queue'},
}
```

- `-Q:1 email_queue` 和 `-Q:2 data_queue` 与 `task_routes` 中的队列名一致，确保任务被正确路由到对应的 Worker。

---

### 总结

| **参数**             | **含义**                      | **示例值**         |
|--------------------|-----------------------------|-----------------|
| `multi`            | 管理多个 Worker                 | -               |
| `start`            | 启动 Worker                   | -               |
| `2`                | Worker 数量                   | 2               |
| `-A PostalSavings` | 指定 Celery 应用                | `PostalSavings` |
| `-Q:1 email_queue` | 第一个 Worker 监听 `email_queue` | `email_queue`   |
| `-Q:2 data_queue`  | 第二个 Worker 监听 `data_queue`  | `data_queue`    |


