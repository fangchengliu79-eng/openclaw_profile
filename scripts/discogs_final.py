#!/usr/bin/env python3
"""
Discogs House音乐每日搜索 - 完整版
包含邮件发送功能
"""

import urllib.request
import urllib.parse
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sys

class DiscogsDaily:
    def __init__(self):
        # Discogs配置
        self.token = 'SPNqBXXqaxguKEtomolGIDuAKNinRnqrJFImObIe'
        
        # 邮件配置（从环境变量读取）
        self.email_to = os.environ.get('EMAIL_TO', '3897451169@qq.com')
        self.email_from = os.environ.get('EMAIL_FROM', '')
        self.email_password = os.environ.get('EMAIL_PASSWORD', '')
        
        # 检查必要的配置
        if not self.email_from or not self.email_password:
            print("❌ 错误: 未设置邮件配置")
            print("请设置以下环境变量:")
            print("export EMAIL_FROM='你的发送邮箱@qq.com'")
            print("export EMAIL_PASSWORD='你的邮箱授权码'")
            sys.exit(1)
    
    def search_latest_house(self):
        """搜索最新House音乐"""
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
        req.add_header('Authorization', f'Discogs token={self.token}')
        req.add_header('User-Agent', 'OpenClawDiscogsBot/1.0')
        
        try:
            print(f"{datetime.now()} - 搜索Discogs最新House音乐...")
            
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
                        'thumb': result.get('thumb', ''),
                        'country': result.get('country', '未知国家'),
                        'format': ', '.join(result.get('format', []))
                    }
                    
                    print(f"✅ 找到音乐: {track_info['title']}")
                    return track_info
                else:
                    print("❌ 未找到结果")
                    return None
                    
        except Exception as e:
            print(f"❌ 搜索失败: {str(e)}")
            return None
    
    def generate_email(self, track_info):
        """生成邮件"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # HTML内容
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Discogs House音乐日报 - {today}</title>
    <style>
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
            text-align: center;
            margin-bottom: 0;
        }}
        .content {{
            background: white;
            padding: 30px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .track-title {{
            color: #2c3e50;
            font-size: 24px;
            margin-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }}
        .track-artist {{
            color: #3498db;
            font-size: 18px;
            margin-bottom: 20px;
        }}
        .info-item {{
            margin-bottom: 12px;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .info-label {{
            font-weight: bold;
            color: #7f8c8d;
            display: inline-block;
            width: 100px;
        }}
        .button {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 20px;
            transition: background 0.3s;
        }}
        .button:hover {{
            background: #2980b9;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #95a5a6;
            font-size: 12px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        }}
        .cover-img {{
            max-width: 200px;
            border-radius: 8px;
            margin: 20px auto;
            display: block;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎵 Discogs House音乐日报</h1>
        <p>每日最新House音乐推荐 - {today}</p>
    </div>
    
    <div class="content">
        <h2 class="track-title">{track_info['title']}</h2>
        <h3 class="track-artist">{track_info['artist']}</h3>
        
        {f'<img src="{track_info["thumb"]}" alt="专辑封面" class="cover-img">' if track_info['thumb'] else ''}
        
        <div class="info-item">
            <span class="info-label">发行年份:</span>
            <span>{track_info['year']}</span>
        </div>
        <div class="info-item">
            <span class="info-label">音乐风格:</span>
            <span>{track_info['style']}</span>
        </div>
        <div class="info-item">
            <span class="info-label">发行国家:</span>
            <span>{track_info['country']}</span>
        </div>
        <div class="info-item">
            <span class="info-label">发行格式:</span>
            <span>{track_info['format']}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Discogs链接:</span>
            <a href="{track_info['url']}">{track_info['url']}</a>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="{track_info['url']}" class="button" target="_blank">🎧 在Discogs上查看详情</a>
        </div>
        
        <div class="footer">
            <p>此邮件由OpenClaw自动化系统发送 | 每天上午10:00自动推送</p>
            <p>搜索条件: House风格 | 按修改日期排序 | 最新发布优先</p>
        </div>
    </div>
</body>
</html>"""
        
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🎵 Discogs House音乐日报 - {today}"
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        
        # 添加HTML内容
        msg.attach(MIMEText(html, 'html'))
        
        return msg
    
    def send_email(self, msg):
        """发送邮件"""
        try:
            # QQ邮箱SMTP配置
            smtp_server = "smtp.qq.com"
            smtp_port = 587
            
            print("正在连接邮件服务器...")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                print("正在登录邮箱...")
                server.login(self.email_from, self.email_password)
                print("正在发送邮件...")
                server.send_message(msg)
            
            print(f"✅ 邮件已成功发送到 {self.email_to}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {str(e)}")
            return False
    
    def run(self):
        """运行主任务"""
        print("="*60)
        print("Discogs House音乐每日搜索任务")
        print("="*60)
        
        # 搜索音乐
        track_info = self.search_latest_house()
        
        if not track_info:
            print("❌ 未找到音乐，任务终止")
            return False
        
        # 生成邮件
        print("正在生成邮件...")
        msg = self.generate_email(track_info)
        
        # 发送邮件
        print("正在发送邮件...")
        success = self.send_email(msg)
        
        if success:
            print(f"\n✅ 任务完成！")
            print(f"   发送时间: {datetime.now()}")
            print(f"   音乐标题: {track_info['title']}")
            print(f"   收件人: {self.email_to}")
        else:
            print("\n❌ 任务失败")
        
        return success

def main():
    """主函数"""
    # 创建任务实例
    task = DiscogsDaily()
    
    # 运行任务
    success = task.run()
    
    # 返回退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()