#!/bin/bash
# Discogs每日任务运行脚本

# 设置环境变量
# 请修改以下变量为你的实际值
export EMAIL_FROM="你的发送邮箱@qq.com"      # 修改为你的QQ邮箱
export EMAIL_PASSWORD="你的邮箱授权码"        # 修改为你的邮箱授权码（不是QQ密码）
export EMAIL_TO="3897451169@qq.com"

# 日志文件
LOG_DIR="/var/log/discogs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/discogs_$(date +%Y%m%d_%H%M%S).log"

echo "=== Discogs每日任务开始: $(date) ===" | tee -a "$LOG_FILE"

# 检查环境变量
if [ -z "$EMAIL_FROM" ] || [ -z "$EMAIL_PASSWORD" ]; then
    echo "❌ 错误: 未设置邮件配置" | tee -a "$LOG_FILE"
    echo "请编辑此脚本设置以下变量:" | tee -a "$LOG_FILE"
    echo "1. EMAIL_FROM: 你的发送邮箱@qq.com" | tee -a "$LOG_FILE"
    echo "2. EMAIL_PASSWORD: 你的邮箱授权码" | tee -a "$LOG_FILE"
    exit 1
fi

# 运行Python脚本
echo "运行Discogs搜索脚本..." | tee -a "$LOG_FILE"
cd "$(dirname "$0")"
python3 discogs_final.py 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 任务成功完成: $(date)" | tee -a "$LOG_FILE"
else
    echo "❌ 任务失败，退出码: $EXIT_CODE" | tee -a "$LOG_FILE"
fi

echo "=== 任务结束: $(date) ===" | tee -a "$LOG_FILE"

# 保留最近7天的日志
find "$LOG_DIR" -name "discogs_*.log" -mtime +7 -delete

exit $EXIT_CODE