#!/usr/bin/env python3
"""
Discogs定时任务专用脚本
用于OpenClaw定时任务执行
"""

import urllib.request
import urllib.parse
import json
import os
from datetime import datetime

def search_discogs():
    """搜索Discogs最新House音乐"""
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
        print(f"🕐 {datetime.now()} - 开始搜索Discogs最新House音乐...")
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                
                track_info = {
                    'title': result.get('title', '未知标题'),
                    'artist': result.get('artist', '未知艺术家'),
                    'year': result.get('year', '未知年份'),
                    'style': ', '.join(result.get('style', ['未知风格'])),
                    'id': result.get('id', 0),
                    'url': f"https://www.discogs.com/release/{result.get('id')}",
                    'country': result.get('country', '未知国家'),
                    'format': ', '.join(result.get('format', []))
                }
                
                print(f"✅ 搜索成功！")
                print(f"   音乐标题: {track_info['title']}")
                print(f"   艺术家: {track_info['artist']}")
                print(f"   发行年份: {track_info['year']}")
                print(f"   音乐风格: {track_info['style']}")
                print(f"   发行国家: {track_info['country']}")
                print(f"   发行格式: {track_info['format']}")
                print(f"   Discogs链接: {track_info['url']}")
                
                return track_info
            else:
                print("❌ 未找到结果")
                return None
                
    except Exception as e:
        print(f"❌ 搜索失败: {str(e)}")
        return None

def check_email_config():
    """检查邮箱配置"""
    email_from = os.environ.get('EMAIL_FROM', '')
    email_password = os.environ.get('EMAIL_PASSWORD', '')
    email_to = os.environ.get('EMAIL_TO', '3897451169@qq.com')
    
    if email_from and email_password:
        print(f"✅ 邮箱配置检查通过")
        print(f"   发送邮箱: {email_from}")
        print(f"   目标邮箱: {email_to}")
        return True
    else:
        print("⚠️  邮箱配置缺失")
        print("   需要设置以下环境变量:")
        print("   export EMAIL_FROM='你的QQ邮箱@qq.com'")
        print("   export EMAIL_PASSWORD='你的邮箱授权码'")
        print("   export EMAIL_TO='3897451169@qq.com' (可选，默认已设置)")
        return False

def generate_report(track_info, email_configured):
    """生成执行报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""
## 📊 Discogs House音乐日报 - 执行报告 ({today})

### 🔍 搜索结果
- **音乐标题:** {track_info['title']}
- **艺术家:** {track_info['artist']}
- **发行年份:** {track_info['year']}
- **音乐风格:** {track_info['style']}
- **发行国家:** {track_info['country']}
- **发行格式:** {track_info['format']}
- **Discogs链接:** {track_info['url']}

### 📧 邮件发送状态
"""
    
    if email_configured:
        report += f"- ✅ **邮件已发送**到 {os.environ.get('EMAIL_TO', '3897451169@qq.com')}"
    else:
        report += """- ⚠️ **邮件未发送** (需要配置邮箱)
  需要设置以下环境变量：
  ```
  export EMAIL_FROM='你的QQ邮箱@qq.com'
  export EMAIL_PASSWORD='你的邮箱授权码'
  export EMAIL_TO='3897451169@qq.com'
  ```

### 🔧 配置说明
1. **获取QQ邮箱授权码：**
   - 登录QQ邮箱网页版
   - 进入"设置" → "账户"
   - 开启"IMAP/SMTP服务"
   - 获取"授权码"

2. **配置环境变量：**
   ```bash
   # 编辑配置文件
   nano /root/.openclaw/workspace/scripts/run_discogs.sh
   
   # 修改以下行：
   export EMAIL_FROM="你的QQ邮箱@qq.com"
   export EMAIL_PASSWORD="你的邮箱授权码"
   ```

3. **手动测试：**
   ```bash
   cd /root/.openclaw/workspace/scripts
   EMAIL_FROM='你的邮箱' EMAIL_PASSWORD='你的授权码' python3 discogs_final.py
   ```

### ⏰ 下次执行
- **时间:** 明天 10:00 (Asia/Shanghai)
- **任务ID:** 991c10f0-38c8-4357-bfbe-a21dc73613e5
"""
    
    return report

def main():
    """主函数"""
    print("="*60)
    print("🎵 Discogs House音乐日报 - 定时任务执行")
    print("="*60)
    
    # 检查邮箱配置
    email_configured = check_email_config()
    
    # 搜索音乐
    track_info = search_discogs()
    
    if track_info:
        # 生成报告
        report = generate_report(track_info, email_configured)
        
        # 保存报告到文件
        report_file = f"/tmp/discogs_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 详细报告已保存到: {report_file}")
        print("\n" + report)
        
        # 如果邮箱已配置，尝试发送邮件
        if email_configured:
            print("\n📧 正在尝试发送邮件...")
            try:
                # 导入邮件发送模块
                import sys
                sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                from discogs_final import DiscogsDaily
                
                task = DiscogsDaily()
                success = task.run()
                
                if success:
                    print("✅ 邮件发送成功！")
                else:
                    print("❌ 邮件发送失败，请检查邮箱配置")
            except Exception as e:
                print(f"❌ 邮件发送错误: {str(e)}")
        else:
            print("\n⚠️  邮件未发送，请配置邮箱信息")
    else:
        print("❌ 搜索失败，任务终止")
    
    print(f"\n🏁 任务执行完成: {datetime.now()}")

if __name__ == "__main__":
    main()