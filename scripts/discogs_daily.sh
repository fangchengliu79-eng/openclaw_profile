#!/bin/bash
# Discogs House音乐每日搜索脚本

# 设置环境变量
export DISCogs_TOKEN="SPNqBXXqaxguKEtomolGIDuAKNinRnqrJFImObIe"
export EMAIL_TO="3897451169@qq.com"
export EMAIL_FROM="你的发送邮箱@qq.com"  # 需要修改
export EMAIL_PASSWORD="你的邮箱授权码"    # 需要修改

# 日志文件
LOG_FILE="/tmp/discogs_daily_$(date +%Y%m%d).log"
echo "=== Discogs每日任务开始: $(date) ===" > "$LOG_FILE"

# 搜索最新House音乐
echo "搜索最新House音乐..." >> "$LOG_FILE"
RESPONSE=$(curl -s -H "Authorization: Discogs token=$DISCogs_TOKEN" \
  "https://api.discogs.com/database/search?q=&type=release&style=House&sort=date_changed&order=desc&per_page=1")

# 解析结果
TITLE=$(echo "$RESPONSE" | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['results'][0]['title'] if data.get('results') else '未找到')")
ARTIST=$(echo "$RESPONSE" | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['results'][0].get('artist', '未知艺术家') if data.get('results') else '未知')")
YEAR=$(echo "$RESPONSE" | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['results'][0].get('year', '未知年份') if data.get('results') else '未知')")
STYLE=$(echo "$RESPONSE" | python3 -c "import sys,json; data=json.load(sys.stdin); styles=data['results'][0].get('style', ['未知']) if data.get('results') else ['未知']; print(', '.join(styles))")
ID=$(echo "$RESPONSE" | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['results'][0]['id'] if data.get('results') else '0')")
URL="https://www.discogs.com/release/$ID"

echo "找到音乐: $TITLE" >> "$LOG_FILE"
echo "艺术家: $ARTIST" >> "$LOG_FILE"
echo "年份: $YEAR" >> "$LOG_FILE"
echo "风格: $STYLE" >> "$LOG_FILE"
echo "链接: $URL" >> "$LOG_FILE"

# 生成邮件内容
HTML_CONTENT=$(cat << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Discogs House音乐日报 - $(date +%Y-%m-%d)</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background: #4a6fa5; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .track-info { background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .button { background: #4a6fa5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎵 Discogs House音乐日报</h1>
        <p>每日最新House音乐推荐 - $(date +%Y-%m-%d)</p>
    </div>
    
    <div class="content">
        <div class="track-info">
            <h2>$TITLE</h2>
            <h3>$ARTIST</h3>
            
            <p><strong>发行年份:</strong> $YEAR</p>
            <p><strong>音乐风格:</strong> $STYLE</p>
            <p><strong>Discogs链接:</strong> <a href="$URL">$URL</a></p>
            
            <p style="margin-top: 20px;">
                <a href="$URL" class="button" target="_blank">🎧 在Discogs上查看详情</a>
            </p>
        </div>
        
        <div style="margin-top: 30px; padding: 15px; background: #f0f0f0; border-radius: 5px;">
            <h4>💡 关于此邮件:</h4>
            <p>此邮件由OpenClaw自动化系统每天上午10:00自动发送。</p>
            <p>系统每天搜索Discogs上最新发布的House风格音乐，并推荐排名第一的结果。</p>
        </div>
    </div>
</body>
</html>
EOF
)

# 发送邮件（这里需要配置邮件发送）
echo "生成邮件内容完成，长度: ${#HTML_CONTENT} 字符" >> "$LOG_FILE"

# 这里可以添加邮件发送逻辑
# 例如使用sendmail或mail命令
# 或者调用Python脚本发送

echo "=== 任务完成: $(date) ===" >> "$LOG_FILE"

# 显示日志
cat "$LOG_FILE"