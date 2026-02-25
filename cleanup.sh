#!/bin/bash
# 递归清理 /xxx/logs/ 下所有服务目录的日志

# 设置根路径
ROOT_PATH="/xxx/logs/"

# 设置阈值
THRESHOLD=30

# 获取当前的磁盘使用百分比
USAGE=$(df -h "$ROOT_PATH" | awk 'NR==2 {print $5}' | sed 's/%//g')

# 检查磁盘使用情况
if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "磁盘使用率为 ${USAGE}%，超过阈值 ${THRESHOLD}%。开始清理..."

    # 递归删除所有包含 202 的目录
    find "$ROOT_PATH" -depth -type d -name '*202*' -exec rm -rf {} +
    
    # 递归删除所有包含 202 的文件
    find "$ROOT_PATH" -type f -name '*202*' -delete

    echo "清理完成"
else
    echo "磁盘使用率为 ${USAGE}%，未超过阈值 ${THRESHOLD}%。不进行删除。"
fi
