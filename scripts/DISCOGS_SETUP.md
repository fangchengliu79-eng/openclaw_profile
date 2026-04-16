# Discogs House音乐日报 - 配置说明

## 📋 任务概述
每天上午10:00自动搜索Discogs上最新发布的House风格音乐，将排名第一的结果发送到你的邮箱。

## 🔧 已完成的配置

### 1. **Discogs API配置**
- ✅ Token: `SPNqBXXqaxguKEtomolGIDuAKNinRnqrJFImObIe`
- ✅ 搜索参数: House风格, 按修改日期排序, 最新优先
- ✅ API测试: 通过

### 2. **脚本文件**
- `discogs_final.py` - 主程序（搜索+邮件发送）
- `discogs_simple.py` - 简化版（仅搜索，测试用）
- `run_discogs.sh` - 包装脚本（包含日志）

### 3. **OpenClaw定时任务**
- **任务ID:** `991c10f0-38c8-4357-bfbe-a21dc73613e5`
- **执行时间:** 每天10:00（亚洲/上海时间）
- **目标邮箱:** `3897451169@qq.com`

## ⚙️ 需要你完成的配置

### 1. **配置QQ邮箱**
```bash
# 编辑脚本文件
nano /root/.openclaw/workspace/scripts/run_discogs.sh

# 修改以下变量：
export EMAIL_FROM="你的QQ邮箱@qq.com"      # 例如: 12345678@qq.com
export EMAIL_PASSWORD="你的邮箱授权码"      # 注意：不是QQ密码！
```

### 2. **获取QQ邮箱授权码**
1. 登录QQ邮箱网页版
2. 进入"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"IMAP/SMTP服务"
5. 按照提示获取"授权码"

### 3. **测试配置**
```bash
# 1. 设置环境变量
export EMAIL_FROM="你的QQ邮箱@qq.com"
export EMAIL_PASSWORD="你的邮箱授权码"

# 2. 测试脚本
cd /root/.openclaw/workspace/scripts
python3 discogs_final.py
```

## 🚀 手动测试命令
```bash
# 完整测试（包含邮件发送）
EMAIL_FROM="你的QQ邮箱@qq.com" \
EMAIL_PASSWORD="你的邮箱授权码" \
python3 /root/.openclaw/workspace/scripts/discogs_final.py

# 仅测试搜索功能（不发送邮件）
python3 /root/.openclaw/workspace/scripts/discogs_simple.py
```

## 📊 检查定时任务状态
```bash
# 查看所有定时任务
openclaw cron list

# 查看Discogs任务详情
openclaw cron list | grep Discogs

# 查看任务运行历史
openclaw cron runs --id 991c10f0-38c8-4357-bfbe-a21dc73613e5
```

## 🔍 故障排除

### 1. **邮件发送失败**
- 检查QQ邮箱授权码是否正确
- 确认SMTP服务已开启
- 检查网络连接

### 2. **API搜索失败**
- 检查Discogs token是否有效
- 确认网络可以访问api.discogs.com
- 查看日志文件 `/var/log/discogs/`

### 3. **定时任务不执行**
```bash
# 检查OpenClaw服务状态
openclaw gateway status

# 检查定时任务是否启用
openclaw cron list
```

## 📧 邮件示例
每天你会收到类似这样的邮件：
```
主题: 🎵 Discogs House音乐日报 - 2026-04-15

内容包含：
- 音乐标题和艺术家
- 发行年份和风格
- 专辑封面（如果有）
- Discogs直接链接
- 精美的HTML格式
```

## ⏰ 执行时间线
- **10:00** - 自动执行搜索
- **10:01** - 生成邮件内容
- **10:02** - 发送到你的邮箱
- **全天** - 你随时可以查看最新House音乐

## 🔄 修改配置
如需修改搜索条件或目标邮箱，编辑以下文件：
- `discogs_final.py` - 修改搜索参数（第40-48行）
- `run_discogs.sh` - 修改邮箱配置（第7-8行）

## 📞 支持
如有问题，请检查：
1. 日志文件: `/var/log/discogs/`
2. OpenClaw日志: `openclaw gateway logs`
3. 脚本输出: 手动运行测试命令

任务ID: `991c10f0-38c8-4357-bfbe-a21dc73613e5`
创建时间: 2026-04-15
下次执行: 明天10:00