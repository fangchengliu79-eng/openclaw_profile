#!/bin/bash
# 测试Discogs脚本的配置

echo "=== Discogs测试脚本 ==="
echo "当前时间: $(date)"
echo ""

# 检查网络连接
echo "1. 检查网络连接..."
ping -c 2 api.discogs.com > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 网络连接正常"
else
    echo "❌ 网络连接失败"
    exit 1
fi

# 检查Discogs token
echo ""
echo "2. 检查Discogs token..."
TOKEN="SPNqBXXqaxguKEtomolGIDuAKNinRnqrJFImObIe"
if [ -n "$TOKEN" ]; then
    echo "✅ Token存在: ${TOKEN:0:10}..."
else
    echo "❌ Token不存在"
    exit 1
fi

# 测试API连接
echo ""
echo "3. 测试Discogs API连接..."
cd /root/.openclaw/workspace/scripts
python3 -c "
import urllib.request
import urllib.parse
import json
from datetime import datetime

token = 'SPNqBXXqaxguKEtomolGIDuAKNinRnqrJFImObIe'
params = {
    'q': '',
    'type': 'release',
    'style': 'House',
    'sort': 'date_changed',
    'order': 'desc',
    'per_page': '1',
    'page': '1'
}

url = 'https://api.discogs.com/database/search?' + urllib.parse.urlencode(params)
req = urllib.request.Request(url)
req.add_header('Authorization', f'Discogs token={token}')
req.add_header('User-Agent', 'OpenClawDiscogsBot/1.0')

try:
    print('正在测试API连接...')
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode())
        if data.get('results') and len(data['results']) > 0:
            result = data['results'][0]
            print(f'✅ API连接成功！')
            print(f'   找到音乐: {result.get(\"title\", \"未知标题\")}')
            print(f'   艺术家: {result.get(\"artist\", \"未知艺术家\")}')
            print(f'   年份: {result.get(\"year\", \"未知年份\")}')
        else:
            print('✅ API连接成功，但未找到结果')
except Exception as e:
    print(f'❌ API连接失败: {str(e)}')
"

# 检查邮件配置
echo ""
echo "4. 检查邮件配置..."
if [ -n "$EMAIL_FROM" ] && [ -n "$EMAIL_PASSWORD" ]; then
    echo "✅ 邮件配置已设置"
    echo "   发件人: $EMAIL_FROM"
    echo "   收件人: 3897451169@qq.com"
else
    echo "⚠️  邮件配置未设置"
    echo "   需要设置以下环境变量:"
    echo "   export EMAIL_FROM='你的发送邮箱@qq.com'"
    echo "   export EMAIL_PASSWORD='你的邮箱授权码'"
fi

echo ""
echo "=== 测试完成 ==="
echo "如需运行完整任务，请设置邮件配置后执行:"
echo "cd /root/.openclaw/workspace/scripts && \\"
echo "EMAIL_FROM='你的发送邮箱@qq.com' \\"
echo "EMAIL_PASSWORD='你的邮箱授权码' \\"
echo "python3 discogs_final.py"