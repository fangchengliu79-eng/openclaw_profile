#!/usr/bin/env python3
"""
Discogs House音乐搜索脚本
每天搜索最新发布的House风格音乐，发送到指定邮箱
"""

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os

class DiscogsHouseSearch:
    def __init__(self):
        # Discogs API配置
        self.discogs_token = "SPNqBXXqaxguKEtomolGIDuAKNinRnqrJFImObIe"
        self.api_base_url = "https://api.discogs.com"
        
        # 邮件配置（QQ邮箱）
        self.smtp_server = "smtp.qq.com"
        self.smtp_port = 587
        self.email_from = "你的发送邮箱@qq.com"  # 需要修改为你的发送邮箱
        self.email_password = "你的邮箱授权码"    # 需要修改为你的邮箱授权码
        self.email_to = "3897451169@qq.com"
        
        # 搜索参数
        self.search_params = {
            'q': '',           # 空搜索词，获取所有
            'type': 'release', # 搜索发行版
            'style': 'House',  # 风格：House
            'sort': 'date_changed',  # 按修改日期排序
            'order': 'desc',   # 降序（最新的在前）
            'per_page': 1,     # 每页1个结果
            'page': 1          # 第一页
        }
    
    def search_top_house_track(self):
        """搜索排名第一的House风格音乐"""
        headers = {
            'Authorization': f'Discogs token={self.discogs_token}',
            'User-Agent': 'OpenClawDiscogsBot/1.0'
        }
        
        try:
            print(f"{datetime.now()} - 正在搜索Discogs最新House音乐...")
            
            response = requests.get(
                f"{self.api_base_url}/database/search",
                params=self.search_params,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('results') and len(data['results']) > 0:
                    result = data['results'][0]
                    
                    # 提取详细信息
                    track_info = {
                        'title': result.get('title', '未知标题'),
                        'artist': result.get('artist', '未知艺术家'),
                        'year': result.get('year', '未知年份'),
                        'genre': ', '.join(result.get('genre', [])),
                        'style': ', '.join(result.get('style', [])),
                        'label': ', '.join(result.get('label', [])),
                        'id': result.get('id'),
                        'url': f"https://www.discogs.com/release/{result.get('id')}",
                        'thumb': result.get('thumb', ''),
                        'country': result.get('country', '未知国家'),
                        'format': ', '.join(result.get('format', []))
                    }
                    
                    print(f"找到结果: {track_info['title']}")
                    return track_info
                else:
                    print("未找到结果")
                    return None
            else:
                print(f"API请求失败: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None
                
        except Exception as e:
            print(f"搜索过程中发生错误: {str(e)}")
            return None
    
    def get_release_details(self, release_id):
        """获取发行版的详细信息"""
        headers = {
            'Authorization': f'Discogs token={self.discogs_token}',
            'User-Agent': 'OpenClawDiscogsBot/1.0'
        }
        
        try:
            response = requests.get(
                f"{self.api_base_url}/releases/{release_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取详细信息失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取详细信息错误: {str(e)}")
            return None
    
    def generate_email_content(self, track_info, release_details=None):
        """生成邮件内容"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 如果有详细信息，提取曲目列表
        tracklist = ""
        if release_details and 'tracklist' in release_details:
            tracklist = "<h4>🎵 曲目列表:</h4><ul>"
            for track in release_details['tracklist'][:10]:  # 只显示前10首
                tracklist += f"<li>{track.get('position', '')} - {track.get('title', '')} ({track.get('duration', '')})</li>"
            tracklist += "</ul>"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Discogs House音乐日报 - {today}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .track-card {{
                    background: white;
                    border-radius: 10px;
                    padding: 25px;
                    margin-bottom: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .track-title {{
                    color: #2c3e50;
                    font-size: 24px;
                    margin-bottom: 10px;
                }}
                .track-artist {{
                    color: #3498db;
                    font-size: 18px;
                    margin-bottom: 15px;
                }}
                .info-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }}
                .info-item {{
                    background: #f8f9fa;
                    padding: 12px;
                    border-radius: 6px;
                }}
                .info-label {{
                    font-weight: bold;
                    color: #7f8c8d;
                    font-size: 12px;
                    text-transform: uppercase;
                    margin-bottom: 5px;
                }}
                .info-value {{
                    color: #2c3e50;
                    font-size: 14px;
                }}
                .track-cover {{
                    max-width: 200px;
                    border-radius: 8px;
                    margin: 20px auto;
                    display: block;
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
                    margin-top: 40px;
                    color: #7f8c8d;
                    font-size: 12px;
                    border-top: 1px solid #eee;
                    padding-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎵 Discogs House音乐日报</h1>
                <p>每日最新House音乐推荐 - {today}</p>
            </div>
            
            <div class="track-card">
                <h2 class="track-title">{track_info['title']}</h2>
                <h3 class="track-artist">{track_info['artist']}</h3>
                
                {f'<img src="{track_info["thumb"]}" alt="专辑封面" class="track-cover">' if track_info['thumb'] else ''}
                
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">发行年份</div>
                        <div class="info-value">{track_info['year']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">音乐风格</div>
                        <div class="info-value">{track_info['style']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">音乐类型</div>
                        <div class="info-value">{track_info['genre']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">发行国家</div>
                        <div class="info-value">{track_info['country']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">发行格式</div>
                        <div class="info-value">{track_info['format']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">发行厂牌</div>
                        <div class="info-value">{track_info['label']}</div>
                    </div>
                </div>
                
                {tracklist}
                
                <div style="text-align: center;">
                    <a href="{track_info['url']}" class="button" target="_blank">🎧 在Discogs上查看详情</a>
                </div>
            </div>
            
            <div class="footer">
                <p>此邮件由OpenClaw自动化系统发送 | 每天上午10:00自动推送</p>
                <p>如需取消订阅或调整设置，请回复此邮件</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def send_email(self, html_content):
        """发送邮件"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🎵 Discogs House音乐日报 - {today}"
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        
        # 添加HTML内容
        msg.attach(MIMEText(html_content, 'html'))
        
        try:
            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.send_message(msg)
            
            print(f"✅ 邮件已成功发送到 {self.email_to}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {str(e)}")
            return False
    
    def run_daily_task(self):
        """每日执行的任务"""
        print(f"\n{'='*60}")
        print(f"{datetime.now()} - 开始执行Discogs House音乐搜索任务")
        print(f"{'='*60}")
        
        # 1. 搜索最新House音乐
        track_info = self.search_top_house_track()
        
        if not track_info:
            print("❌ 未找到合适的音乐，任务终止")
            return False
        
        # 2. 获取详细信息（可选）
        release_details = None
        if track_info['id']:
            print("正在获取详细信息...")
            release_details = self.get_release_details(track_info['id'])
        
        # 3. 生成邮件内容
        print("正在生成邮件内容...")
        email_content = self.generate_email_content(track_info, release_details)
        
        # 4. 发送邮件
        print("正在发送邮件...")
        success = self.send_email(email_content)
        
        if success:
            print(f"✅ 任务完成！已发送: {track_info['title']}")
        else:
            print("❌ 任务失败")
        
        return success

def main():
    """主函数"""
    # 检查必要的环境变量
    required_vars = ['EMAIL_FROM', 'EMAIL_PASSWORD']
    missing_vars = [var for var in required_vars if var not in os.environ]
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        print("请设置以下环境变量:")
        print("export EMAIL_FROM='你的发送邮箱@qq.com'")
        print("export EMAIL_PASSWORD='你的邮箱授权码'")
        return
    
    # 创建搜索器实例
    searcher = DiscogsHouseSearch()
    
    # 设置邮箱配置
    searcher.email_from = os.environ['EMAIL_FROM']
    searcher.email_password = os.environ['EMAIL_PASSWORD']
    
    # 执行任务
    searcher.run_daily_task()

if __name__ == "__main__":
    main()